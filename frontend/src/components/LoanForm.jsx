import {
  checkingAccountOptions,
  creditHistoryOptions,
  loanPurposeOptions,
  savingsAccountOptions,
  employmentDurationOptions,
  installmentRateOptions,
  personalStatusOptions,
  guarantorOptions,
  residenceDurationOptions,
  propertyOptions,
  otherInstallmentPlanOptions,
  housingOptions,
  existingCreditOptions,
  jobOptions,
  dependentsOptions,
  telephoneOptions,
  foreignWorkerOptions,
} from "../data/dropdownOptions";

const initialFormData = {
  checking_account: 3,
  loan_duration_months: 24,
  credit_history: 3,
  loan_purpose: 2,
  loan_amount: 5000,
  savings_account: 3,
  employment_years: 3,
  installment_rate_percent: 3,
  personal_status: 3,
  guarantors: 1,
  years_at_residence: 3,
  property_assets: 4,
  age: 35,
  other_installment_plans: 3,
  housing_type: 3,
  existing_credit_count: 1,
  job: 3,
  dependents: 2,
  telephone_available: 2,
  foreign_worker: 1,
};
function SliderField({
  label,
  name,
  value,
  onChange,
  min,
  max,
  step = 1,
  suffix = "",
  helperText,
}) {
  return (
    <label className="form-field slider-field">
      <div className="slider-label-row">
        <span>{label}</span>
        <strong>
          {Number(value).toLocaleString()}
          {suffix}
        </strong>
      </div>

      <input
        type="range"
        name={name}
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={onChange}
      />

      <div className="slider-range">
        <small>
          {min.toLocaleString()}
          {suffix}
        </small>
        <small>
          {max.toLocaleString()}
          {suffix}
        </small>
      </div>

      {helperText && <small>{helperText}</small>}
    </label>
  );
}

function SelectField({ label, name, value, options, onChange }) {
  return (
    <label className="form-field">
      <span>{label}</span>

      <select name={name} value={value} onChange={onChange}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function NumberField({
  label,
  name,
  value,
  onChange,
  min,
  max,
  step = 1,
  helperText,
}) {
  return (
    <label className="form-field">
      <span>{label}</span>

      <input
        type="number"
        name={name}
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={onChange}
        required
      />

      {helperText && <small>{helperText}</small>}
    </label>
  );
}

function LoanForm({ formData, setFormData, onSubmit, onReset, loading }) {
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: Number(value),
    }));
  };

  const handleReset = () => {
    setFormData(initialFormData);
    onReset();
  };

  return (
    <form className="loan-form" onSubmit={onSubmit}>
      <div className="form-heading">
        <div>
          <p className="section-label">Applicant Assessment</p>
          <h2>Loan Application Details</h2>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={handleReset}
          disabled={loading}
        >
          Reset
        </button>
      </div>

      <h3>Loan Information</h3>

      <div className="form-grid">
        <SliderField
            label="Loan Amount"
            name="loan_amount"
            value={formData.loan_amount}
            min={250}
            max={18424}
            step={50}
            suffix=" DM"
            onChange={handleChange}
            helperText="Supported model range"
        />

        <SliderField
            label="Loan Duration"
            name="loan_duration_months"
            value={formData.loan_duration_months}
            min={4}
            max={72}
            step={1}
            suffix=" months"
            onChange={handleChange}
            helperText="Supported model range"
        />

        <SelectField
          label="Loan Purpose"
          name="loan_purpose"
          value={formData.loan_purpose}
          options={loanPurposeOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Installment Rate"
          name="installment_rate_percent"
          value={formData.installment_rate_percent}
          options={installmentRateOptions}
          onChange={handleChange}
        />
      </div>

      <h3>Financial Profile</h3>

      <div className="form-grid">
        <SelectField
          label="Checking Account"
          name="checking_account"
          value={formData.checking_account}
          options={checkingAccountOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Savings Account"
          name="savings_account"
          value={formData.savings_account}
          options={savingsAccountOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Credit History"
          name="credit_history"
          value={formData.credit_history}
          options={creditHistoryOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Existing Credits"
          name="existing_credit_count"
          value={formData.existing_credit_count}
          options={existingCreditOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Other Installment Plans"
          name="other_installment_plans"
          value={formData.other_installment_plans}
          options={otherInstallmentPlanOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Property"
          name="property_assets"
          value={formData.property_assets}
          options={propertyOptions}
          onChange={handleChange}
        />
      </div>

      <h3>Personal and Employment Information</h3>

      <div className="form-grid">
        <NumberField
          label="Age"
          name="age"
          value={formData.age}
          min={18}
          max={100}
          onChange={handleChange}
        />

        <SelectField
          label="Employment Duration"
          name="employment_years"
          value={formData.employment_years}
          options={employmentDurationOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Job"
          name="job"
          value={formData.job}
          options={jobOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Personal Status"
          name="personal_status"
          value={formData.personal_status}
          options={personalStatusOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Other Debtors"
          name="guarantors"
          value={formData.guarantors}
          options={guarantorOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Present Residence"
          name="years_at_residence"
          value={formData.years_at_residence}
          options={residenceDurationOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Housing"
          name="housing_type"
          value={formData.housing_type}
          options={housingOptions}
          onChange={handleChange}
        />

        <SelectField
          label="People Financially Liable"
          name="dependents"
          value={formData.dependents}
          options={dependentsOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Telephone"
          name="telephone_available"
          value={formData.telephone_available}
          options={telephoneOptions}
          onChange={handleChange}
        />

        <SelectField
          label="Foreign Worker"
          name="foreign_worker"
          value={formData.foreign_worker}
          options={foreignWorkerOptions}
          onChange={handleChange}
        />
      </div>

      <button className="primary-button" type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Assess Loan Application"}
      </button>
    </form>
  );
}

export { initialFormData };
export default LoanForm;