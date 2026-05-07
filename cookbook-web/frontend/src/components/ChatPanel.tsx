import { useEffect, useRef, useState } from "react";
import { Send, RotateCcw, X, MessageSquare, ChevronRight, Square } from "lucide-react";
import clsx from "clsx";
import { useStreamChat } from "@/hooks/useStreamChat";
import { ChatMessageView } from "./ChatMessage";
import { fetchHealth, type HealthResp } from "@/lib/api";

interface Props {
  currentPage: string | null;
  onSourceClick: (path: string) => void;
}

export function ChatPanel({ currentPage, onSourceClick }: Props) {
  const [open, setOpen] = useState(true);
  const [draft, setDraft] = useState("");
  const [health, setHealth] = useState<HealthResp | null>(null);
  const { turns, streaming, error, send, cancel, reset } = useStreamChat();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchHealth().then(setHealth).catch(() => undefined);
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [turns]);

  const submit = () => {
    if (!draft.trim() || streaming) return;
    send(draft, currentPage ?? undefined);
    setDraft("");
  };

  if (!open) {
    return (
      <button
        className="fixed bottom-6 right-6 bg-accent-orange text-cream rounded-full p-4 shadow-lg hover:scale-105 transition-transform"
        onClick={() => setOpen(true)}
        title="開啟助教"
      >
        <MessageSquare className="w-6 h-6" />
      </button>
    );
  }

  return (
    <aside
      className={clsx(
        "shrink-0 border-l border-lightGray bg-cream/80 flex flex-col",
        "w-[380px]"
      )}
    >
      <div className="px-4 py-3 border-b border-lightGray flex items-center justify-between">
        <div>
          <h3 className="font-display font-bold text-base">🤖 Cookbook 助教</h3>
          {health && (
            <p className="text-xs text-midGray">
              {health.llm_format} · {health.llm_model} · {health.chunks} chunks
              {health.embeddings_loaded ? " · RAG ✅" : " · RAG ❌"}
            </p>
          )}
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={reset}
            className="p-1.5 rounded hover:bg-lightGray text-midGray"
            title="重置對話"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={() => setOpen(false)}
            className="p-1.5 rounded hover:bg-lightGray text-midGray"
            title="收合"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-3 py-3 flex flex-col gap-3">
        {turns.length === 0 && (
          <div className="text-sm text-midGray space-y-2">
            <p>💡 試試這些問題：</p>
            <ul className="list-disc pl-5 space-y-1">
              <li>哪個 skill 最容易上手？</li>
              <li>slack-gif-creator 的 easing 函式有哪些？</li>
              <li>幫我比較 docx 與 pptx 的編輯流程差異</li>
              <li>web-artifacts-builder 跟 frontend-design 的關係是什麼？</li>
            </ul>
            {currentPage && (
              <p className="mt-3 p-2 bg-lightGray/60 rounded text-xs">
                目前頁面：<code>{currentPage}</code> 將自動帶入 context
              </p>
            )}
          </div>
        )}

        {turns.map((turn, i) => (
          <ChatMessageView key={i} turn={turn} onSourceClick={onSourceClick} />
        ))}

        {error && <p className="text-red-600 text-sm">⚠ {error}</p>}
      </div>

      <div className="p-3 border-t border-lightGray">
        <div className="flex gap-2">
          <textarea
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                submit();
              }
            }}
            placeholder="按 Enter 送出（Shift+Enter 換行）"
            rows={2}
            className="flex-1 resize-none border border-lightGray rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent-orange/50 bg-cream"
            disabled={streaming}
          />
          {streaming ? (
            <button
              onClick={cancel}
              className="bg-midGray text-cream rounded-lg px-3 hover:bg-ink"
              title="停止"
            >
              <Square className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={submit}
              disabled={!draft.trim()}
              className="bg-accent-orange text-cream rounded-lg px-3 hover:opacity-90 disabled:opacity-40"
              title="送出"
            >
              <Send className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
