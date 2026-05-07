import type { ChatTurn } from "@/hooks/useStreamChat";
import { FileText } from "lucide-react";

interface Props {
  turn: ChatTurn;
  onSourceClick?: (path: string) => void;
}

export function ChatMessageView({ turn, onSourceClick }: Props) {
  const isUser = turn.role === "user";
  return (
    <div className={`flex flex-col ${isUser ? "items-end" : "items-start"} gap-1`}>
      <div className={isUser ? "chat-bubble-user" : "chat-bubble-assistant"}>
        {turn.content || (isUser ? "" : <span className="text-midGray italic">思考中...</span>)}
      </div>

      {!isUser && turn.sources && turn.sources.length > 0 && (
        <div className="mt-1 max-w-[85%]">
          <p className="text-xs text-midGray mb-1">📎 參考來源：</p>
          <div className="flex flex-col gap-1">
            {turn.sources.slice(0, 5).map((s, i) => (
              <button
                key={i}
                onClick={() => onSourceClick?.(s.file_path)}
                className="text-xs text-accent-blue hover:text-accent-orange flex items-center gap-1 text-left"
                title={`相關度 ${s.score.toFixed(3)}`}
              >
                <FileText className="w-3 h-3 shrink-0" />
                <span className="truncate">{s.file_path} <span className="text-midGray">· {s.heading}</span></span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
