import { useState } from "react";
import clsx from "clsx";
import { ChevronDown, ChevronRight, BookOpen } from "lucide-react";
import type { CookbookTree } from "@/lib/api";

interface Props {
  tree: CookbookTree | null;
  currentPath: string | null;
  onSelect: (path: string) => void;
}

const CATEGORY_ICONS: Record<string, string> = {
  "01-document-skills": "📄",
  "02-creative-skills": "🎨",
  "03-dev-technical-skills": "🛠️",
  "04-enterprise-skills": "🏢",
};

export function Sidebar({ tree, currentPath, onSelect }: Props) {
  const [open, setOpen] = useState<Record<string, boolean>>({});

  if (!tree) {
    return (
      <aside className="w-72 shrink-0 border-r border-lightGray bg-cream/60 p-4 text-sm text-midGray">
        載入目錄中...
      </aside>
    );
  }

  return (
    <aside className="w-72 shrink-0 border-r border-lightGray bg-cream/60 overflow-y-auto">
      <div className="px-4 py-4 border-b border-lightGray flex items-center gap-2">
        <BookOpen className="w-5 h-5 text-accent-orange" />
        <h2 className="font-display font-bold text-lg">Cookbook 目錄</h2>
      </div>

      <nav className="p-2 space-y-1">
        {tree.root_files.map((f) => (
          <button
            key={f.path}
            className={clsx("tree-link w-full text-left", currentPath === f.path && "active")}
            onClick={() => onSelect(f.path)}
          >
            {f.title}
          </button>
        ))}

        {tree.categories.map((cat) => {
          const expanded = open[cat.slug] ?? true;
          const icon = CATEGORY_ICONS[cat.slug] ?? "📁";
          return (
            <div key={cat.slug} className="mt-2">
              <button
                className="flex items-center w-full px-2 py-1.5 text-sm font-semibold hover:bg-lightGray rounded"
                onClick={() => setOpen((s) => ({ ...s, [cat.slug]: !expanded }))}
              >
                {expanded ? <ChevronDown className="w-4 h-4 mr-1" /> : <ChevronRight className="w-4 h-4 mr-1" />}
                <span className="mr-1.5">{icon}</span>
                <span className="truncate">{cat.title}</span>
              </button>
              {expanded && (
                <div className="ml-4 border-l border-lightGray pl-2 mt-1 space-y-0.5">
                  {cat.files.map((f) => (
                    <button
                      key={f.path}
                      className={clsx(
                        "tree-link w-full text-left",
                        currentPath === f.path && "active"
                      )}
                      onClick={() => onSelect(f.path)}
                    >
                      {f.title}
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>
    </aside>
  );
}
