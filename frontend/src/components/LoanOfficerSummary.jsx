function SummaryItem({ label, value }) {
  return (
    <div className="summary-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function LoanOfficerSummary({ summary }) {
  if (!summary) {
    return null;
  }

  return (
    <section className="loan-officer-card">
      <div className="summary-heading">
        <div>
          <p className="section-label">Internal Decision Support</p>
          <h3>Loan Officer Summary</h3>
        </div>

        <span className="internal-badge">Internal</span>
      </div>

      <div className="summary-section">
        <h4>Model Assessment</h4>

        <div className="summary-grid">
          <SummaryItem
            label="Model Decision"
            value={summary.model_decision}
          />

          <SummaryItem
            label="Approval Probability"
            value={`${(summary.approval_probability * 100).toFixed(2)}%`}
          />

          <SummaryItem
            label="Risk Probability"
            value={`${(summary.risk_probability * 100).toFixed(2)}%`}
          />

          <SummaryItem
            label="Risk Level"
            value={summary.risk_level}
          />

          <SummaryItem
            label="Confidence"
            value={summary.confidence}
          />
        </div>
      </div>

      <div className="summary-section">
        <h4>Loan Request</h4>

        <div className="summary-grid">
          <SummaryItem
            label="Requested Amount"
            value={`${summary.requested_loan_amount.toLocaleString()} DM`}
          />

          <SummaryItem
            label="Duration"
            value={`${summary.requested_duration_months} months`}
          />

          <SummaryItem
            label="Purpose"
            value={summary.loan_purpose}
          />
        </div>
      </div>

      <div className="summary-section">
        <h4>Applicant Profile</h4>

        <div className="summary-grid">
          <SummaryItem
            label="Checking Account"
            value={summary.checking_account}
          />

          <SummaryItem
            label="Savings"
            value={summary.savings_account}
          />

          <SummaryItem
            label="Credit History"
            value={summary.credit_history}
          />

          <SummaryItem
            label="Employment Duration"
            value={summary.employment_duration}
          />

          <SummaryItem
            label="Existing Credits"
            value={summary.existing_credits}
          />

          <SummaryItem
            label="Housing"
            value={summary.housing}
          />

          <SummaryItem
            label="Property"
            value={summary.property}
          />

          <SummaryItem
            label="Job"
            value={summary.job}
          />
        </div>
      </div>
    </section>
  );
}

export default LoanOfficerSummary;