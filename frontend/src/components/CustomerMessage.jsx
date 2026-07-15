function CustomerMessage({ message }) {
  if (!message) {
    return null;
  }

  return (
    <section className="customer-message-card">
      <p className="section-label">Customer Communication</p>
      <h3>Preliminary Assessment Message</h3>
      <p>{message}</p>
    </section>
  );
}

export default CustomerMessage;