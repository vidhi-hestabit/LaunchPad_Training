class ContextBuilder:
    def __init__(self):
        pass
    def deduplicate(self, docs):
        seen = set()
        unique_docs = []
        for d in docs:
            text = d.get("text", "")
            if text and text not in seen:
                seen.add(text)
                unique_docs.append(d)
        return unique_docs

    def build(self, docs, k=5):
        
        docs = self.deduplicate(docs)
        docs = docs[:k]
        context_parts = []
        for d in docs:
            source = d.get("metadata", {}).get("source", "unknown")
            text = d.get("text", "")

            context_parts.append(
                f"SOURCE: {source}\nTEXT:\n{text}"
            )

        return "\n\n".join(context_parts)
