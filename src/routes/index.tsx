import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef } from "react";

import "../fairprocess/fairprocess.css";
import markup from "../fairprocess/markup.html?raw";

const title = "FairProcess — Process Integrity Infrastructure";
const description =
  "Case, evidence, and compliance workspace for agencies: dashboards, timelines, communications, rules, and Policy Studio.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    document.body.classList.add("fp-app-body");

    const groups: Array<[string, (el: Element) => void]> = [
      [
        ".fp-nav-item",
        (el) => {
          const page = (el as HTMLElement).dataset.page;
          if (!page) return;
          root.querySelectorAll(".fp-page").forEach((p) => p.classList.remove("active"));
          root.querySelector(`#page-${page}`)?.classList.add("active");
        },
      ],
      [".fp-ps-tab", () => {}],
      [".fp-ps-sidebar-tab", () => {}],
      [".fp-ps-rule", () => {}],
      [".fp-ps-page", () => {}],
    ];

    const cleanups: Array<() => void> = [];
    for (const [selector, extra] of groups) {
      const items = Array.from(root.querySelectorAll(selector));
      items.forEach((item) => {
        const onClick = () => {
          if (selector === ".fp-ps-page" && item.textContent?.trim() === "…") return;
          if (selector === ".fp-nav-item" && !(item as HTMLElement).dataset.page) return;
          items.forEach((i) => i.classList.remove("active"));
          item.classList.add("active");
          extra(item);
        };
        item.addEventListener("click", onClick);
        cleanups.push(() => item.removeEventListener("click", onClick));
      });
    }

    return () => {
      document.body.classList.remove("fp-app-body");
      cleanups.forEach((fn) => fn());
    };
  }, []);

  return <div ref={rootRef} dangerouslySetInnerHTML={{ __html: markup }} />;
}
