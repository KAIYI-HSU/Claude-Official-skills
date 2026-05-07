import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypePrism from "rehype-prism-plus";
import rehypeSlug from "rehype-slug";
import { fetchPage } from "@/lib/api";
import { CodeBlock } from "./CodeBlock";

interface Props {
  path: string | null;
}

export function MarkdownView({ path }: Props) {
  const [content, setContent] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!path) {
      setContent("");
      return;
    }
    setLoading(true);
    setError(null);
    fetchPage(path)
      .then((p) => setContent(p.content))
      .catch((e) => setError(e.message ?? "載入失敗"))
      .finally(() => setLoading(false));
  }, [path]);

  if (!path) {
    return (
      <main className="flex-1 flex items-center justify-center text-midGray">
        <div className="text-center">
          <p className="text-2xl mb-2">📚</p>
          <p>從左側選一個 skill 開始學習</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex-1 overflow-y-auto px-8 py-6">
      <div className="max-w-3xl mx-auto markdown">
        {loading && <p className="text-midGray">載入中...</p>}
        {error && <p className="text-red-600">錯誤：{error}</p>}
        {!loading && !error && (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeSlug, [rehypePrism, { ignoreMissing: true }]]}
            components={{
              pre: ({ children, className }) => <CodeBlock className={className}>{children}</CodeBlock>,
            }}
          >
            {content}
          </ReactMarkdown>
        )}
      </div>
    </main>
  );
}
