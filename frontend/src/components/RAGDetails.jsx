import { useState } from "react";

function cleanPolicyText(text) {
  return text
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/\*\*/g, "")
    .replace(/^\s*[-*]\s+/gm, "• ")
    .trim();
}

function getRelevanceLabel(score) {
  if (score >= 0.75) {
    return "High Match";
  }

  if (score >= 0.55) {
    return "Relevant";
  }

  return "Possible Match";
}

function getRetrievalReason(policy) {
  const source = policy.source.toLowerCase();

  if (source.includes("preliminary_assessment")) {
    return "Preliminary assessment and final-decision wording";
  }

  if (source.includes("customer_communication")) {
    return "Customer communication and disclosure requirements";
  }

  if (source.includes("unsupported_claims")) {
    return "Unsupported promises and institutional claims";
  }

  return "Relevant customer communication policy";
}

function PolicyCard({ policy, index }) {
  const [expanded, setExpanded] = useState(false);

  const relevancePercentage = Math.round(policy.score * 100);

  return (
    <article className="rag-policy-card">
      <button
        type="button"
        className="rag-policy-toggle"
        onClick={() => setExpanded((current) => !current)}
        aria-expanded={expanded}
      >
        <div className="rag-policy-header">
          <div className="rag-policy-source">
            <span className="rag-policy-number">
              Retrieved Policy {index + 1}
            </span>

            <strong>{policy.source}</strong>

            <small>Chunk ID: {policy.id}</small>
          </div>

          <div className="rag-policy-header-actions">
            <div className="relevance-score">
              <span>{getRelevanceLabel(policy.score)}</span>
              <strong>{relevancePercentage}%</strong>
              <small>Relevance</small>
            </div>

            <span className="rag-chevron" aria-hidden="true">
              {expanded ? "▲" : "▼"}
            </span>
          </div>
        </div>
      </button>

      <div className="retrieval-reason">
        <span>Retrieved because</span>
        <strong>✓ {getRetrievalReason(policy)}</strong>
      </div>

      <div className="rag-usage-badge">
        Used by Communication Agent ✓
      </div>

      {expanded && (
        <div className="rag-policy-expanded-content">
          <p className="rag-policy-text">
            {cleanPolicyText(policy.text)}
          </p>
        </div>
      )}
    </article>
  );
}

function RAGDetails({ ragMetadata }) {
  const [showQuery, setShowQuery] = useState(false);

  if (!ragMetadata) {
    return null;
  }

  return (
    <section className="details-section rag-details-section">
      <div className="rag-heading">
        <div>
          <p className="section-label">Retrieval Transparency</p>
          <h3>RAG Policy Retrieval</h3>
        </div>

        <span className="rag-count-badge">
          {ragMetadata.retrieved_count} chunks
        </span>
      </div>

      <div className="rag-pipeline-summary">
        <div>
          <span>Retrieved</span>
          <strong>
            {ragMetadata.retrieved_count} of{" "}
            {ragMetadata.total_indexed_chunks} policy chunks
          </strong>
        </div>

        <div>
          <span>Embedding Model</span>
          <strong>{ragMetadata.embedding_model}</strong>
        </div>

        <div>
          <span>Generation Usage</span>
          <strong>Used by Communication Agent ✓</strong>
        </div>
      </div>

      <button
        className="rag-query-toggle"
        type="button"
        onClick={() => setShowQuery((current) => !current)}
        aria-expanded={showQuery}
      >
        <span>
          {showQuery
            ? "Hide Semantic Retrieval Query"
            : "Show Semantic Retrieval Query"}
        </span>

        <span aria-hidden="true">
          {showQuery ? "▲" : "▼"}
        </span>
      </button>

      {showQuery && (
        <div className="rag-query-box">
          <span>Semantic Retrieval Query</span>
          <p>{ragMetadata.query}</p>
        </div>
      )}

      <div className="rag-policy-list">
        {ragMetadata.policies.map((policy, index) => (
          <PolicyCard
            key={policy.id}
            policy={policy}
            index={index}
          />
        ))}
      </div>

      <p className="rag-score-note">
        Relevance scores represent semantic similarity used for retrieval
        ranking. They are not factual-accuracy or confidence percentages.
      </p>
    </section>
  );
}

export default RAGDetails;