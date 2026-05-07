import { useState } from "react";
import { Copy, Check } from "lucide-react";

interface Props {
  children?: React.ReactNode;
  className?: string;
}

/**
 * Renders <pre><code> blocks with a copy button. Used by react-markdown's `pre` override.
 */
export function CodeBlock({ children, className }: Props) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const node = document.activeElement?.closest("div.code-wrapper")?.querySelector("code");
    const text = node?.textContent ?? "";
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* ignore */
    }
  };

  return (
    <div className="relative code-wrapper group">
      <button
        type="button"
        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-cream/10 hover:bg-cream/20 text-cream rounded px-2 py-1 text-xs flex items-center gap-1"
        onClick={handleCopy}
        title="複製"
      >
        {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
        {copied ? "已複製" : "複製"}
      </button>
      <pre className={className}>{children}</pre>
    </div>
  );
}
