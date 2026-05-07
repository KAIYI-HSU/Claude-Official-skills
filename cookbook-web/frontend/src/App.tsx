import { useEffect, useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { MarkdownView } from "./components/MarkdownView";
import { ChatPanel } from "./components/ChatPanel";
import { fetchTree, type CookbookTree } from "./lib/api";

const DEFAULT_PATH = "README.md";

export default function App() {
  const [tree, setTree] = useState<CookbookTree | null>(null);
  const [currentPath, setCurrentPath] = useState<string | null>(null);
  const [treeError, setTreeError] = useState<string | null>(null);

  useEffect(() => {
    fetchTree()
      .then((t) => {
        setTree(t);
        const initial = window.location.hash.replace(/^#/, "") || DEFAULT_PATH;
        setCurrentPath(initial);
      })
      .catch((e) => setTreeError(e.message ?? "目錄載入失敗"));
  }, []);

  useEffect(() => {
    if (currentPath) {
      window.location.hash = currentPath;
    }
  }, [currentPath]);

  return (
    <div className="h-full flex flex-col">
      <header className="border-b border-lightGray bg-ink text-cream px-6 py-3 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-xl font-display font-bold">📘 Cookbook Web</span>
          <span className="text-sm text-midGray hidden md:inline">Claude Skills 繁中學習手冊</span>
        </div>
        <div className="text-xs text-midGray">企業內離線部署版 · v1</div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <Sidebar tree={tree} currentPath={currentPath} onSelect={setCurrentPath} />
        {treeError ? (
          <main className="flex-1 flex items-center justify-center text-red-600">
            ⚠ 目錄載入失敗：{treeError}
          </main>
        ) : (
          <MarkdownView path={currentPath} />
        )}
        <ChatPanel currentPage={currentPath} onSourceClick={setCurrentPath} />
      </div>
    </div>
  );
}
