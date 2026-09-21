<template>
  <section class="dashboard">
    <div class="dashboard-heading">
      <p class="eyebrow">
        Overview
      </p>

      <h1>Dashboard</h1>

      <p>
        Manage your SellX marketplace
        from here.
      </p>
    </div>

    <div class="dashboard-grid">
      <article class="dashboard-card">
        <div class="card-icon">
          📦
        </div>

        <h2>Products</h2>

        <p>
          Create, edit and manage
          marketplace listings.
        </p>

        <span>
          Product management is next.
        </span>
      </article>

      <article class="dashboard-card">
        <div class="card-icon">
          🗂️
        </div>

        <h2>Categories</h2>

        <p>
          Organize listings into
          marketplace categories.
        </p>

        <span>
          Categories are connected.
        </span>
      </article>

      <article class="dashboard-card">
        <div class="card-icon">
          🖼️
        </div>

        <h2>Product images</h2>

        <p>
          Product photos are stored
          securely in Supabase Storage.
        </p>

        <span>
          Multiple images supported.
        </span>
      </article>
    </div>
  </section>
</template>


<style scoped>
.dashboard-heading {
  margin-bottom: 32px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #777;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.dashboard-heading h1 {
  margin: 0 0 8px;
  font-size: 34px;
}

.dashboard-heading > p:last-child {
  margin: 0;
  color: #666;
}

.dashboard-grid {
  display: grid;
  grid-template-columns:
    repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.dashboard-card {
  min-height: 210px;
  padding: 24px;
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  background: #fff;
}

.card-icon {
  margin-bottom: 24px;
  font-size: 25px;
}

.dashboard-card h2 {
  margin: 0 0 9px;
  font-size: 18px;
}

.dashboard-card p {
  margin: 0 0 18px;
  color: #666;
  line-height: 1.6;
}

.dashboard-card span {
  color: #888;
  font-size: 12px;
}

@media (max-width: 1000px) {
  .dashboard-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 650px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>