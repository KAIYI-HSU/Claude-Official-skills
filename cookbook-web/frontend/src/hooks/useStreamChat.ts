import { useCallback, useRef, useState } from "react";
import { streamChat, type ChatMessage, type ChatSource } from "@/lib/api";

export interface ChatTurn {
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}

export function useStreamChat() {
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const send = useCallback(
    async (text: string, currentPage?: string) => {
      if (!text.trim() || streaming) return;
      setError(null);

      const next: ChatTurn[] = [...turns, { role: "user", content: text }, { role: "assistant", content: "" }];
      setTurns(next);
      setStreaming(true);

      const messages: ChatMessage[] = next
        .filter((t) => !(t.role === "assistant" && t.content === ""))
        .map((t) => ({ role: t.role, content: t.content }));

      const controller = new AbortController();
      abortRef.current = controller;

      try {
        await streamChat({
          messages,
          currentPage,
          signal: controller.signal,
          onSources: (s) =>
            setTurns((prev) => {
              const copy = [...prev];
              const last = copy[copy.length - 1];
              if (last?.role === "assistant") last.sources = s;
              return copy;
            }),
          onToken: (tok) =>
            setTurns((prev) => {
              const copy = [...prev];
              const last = copy[copy.length - 1];
              if (last?.role === "assistant") last.content += tok;
              return copy;
            }),
          onError: (e) => setError(e),
        });
      } catch (e) {
        if ((e as Error).name !== "AbortError") setError((e as Error).message);
      } finally {
        setStreaming(false);
        abortRef.current = null;
      }
    },
    [turns, streaming]
  );

  const cancel = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  const reset = useCallback(() => {
    cancel();
    setTurns([]);
    setError(null);
  }, [cancel]);

  return { turns, streaming, error, send, cancel, reset };
}
