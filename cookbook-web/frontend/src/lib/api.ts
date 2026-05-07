export interface TreeFile {
  path: string;
  title: string;
}

export interface TreeCategory {
  slug: string;
  title: string;
  files: TreeFile[];
}

export interface CookbookTree {
  root_files: TreeFile[];
  categories: TreeCategory[];
}

export interface PageContent {
  path: string;
  content: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatSource {
  file_path: string;
  heading: string;
  score: number;
}

export interface HealthResp {
  status: string;
  embeddings_loaded: boolean;
  chunks: number;
  llm_format: string;
  llm_model: string;
}

const API = "/api";

export async function fetchTree(): Promise<CookbookTree> {
  const r = await fetch(`${API}/cookbook/tree`);
  if (!r.ok) throw new Error("tree fetch failed");
  return r.json();
}

export async function fetchPage(path: string): Promise<PageContent> {
  const r = await fetch(`${API}/cookbook/page?path=${encodeURIComponent(path)}`);
  if (!r.ok) throw new Error("page fetch failed");
  return r.json();
}

export async function fetchHealth(): Promise<HealthResp> {
  const r = await fetch(`${API}/health`);
  if (!r.ok) throw new Error("health fetch failed");
  return r.json();
}

export interface StreamChatOpts {
  messages: ChatMessage[];
  currentPage?: string;
  onSources?: (sources: ChatSource[]) => void;
  onToken?: (token: string) => void;
  onDone?: () => void;
  onError?: (error: string) => void;
  signal?: AbortSignal;
}

/**
 * Streams chat tokens using fetch + manual SSE parsing.
 * The backend emits:
 *   event: sources\ndata: [...]
 *   data: "token-chunk"
 *   event: done\ndata: {}
 */
export async function streamChat(opts: StreamChatOpts): Promise<void> {
  const resp = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      messages: opts.messages,
      current_page: opts.currentPage ?? null,
    }),
    signal: opts.signal,
  });

  if (!resp.ok || !resp.body) {
    opts.onError?.(`HTTP ${resp.status}`);
    return;
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let idx: number;
    // SSE events are separated by blank lines
    while ((idx = buffer.indexOf("\n\n")) !== -1) {
      const raw = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);

      let event = "message";
      let dataLines: string[] = [];
      for (const line of raw.split("\n")) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
      }
      const data = dataLines.join("\n");
      if (!data) continue;

      try {
        const parsed = JSON.parse(data);
        if (event === "sources") {
          opts.onSources?.(parsed as ChatSource[]);
        } else if (event === "done") {
          opts.onDone?.();
          return;
        } else {
          opts.onToken?.(typeof parsed === "string" ? parsed : String(parsed));
        }
      } catch {
        // ignore malformed
      }
    }
  }
  opts.onDone?.();
}
