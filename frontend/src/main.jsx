import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowLeft,
  BadgeCheck,
  Boxes,
  Check,
  CreditCard,
  LogOut,
  PackageCheck,
  Search,
  ShieldCheck,
  ShoppingBag,
  ShoppingCart,
  Sparkles,
  Truck,
  UserPlus,
} from "lucide-react";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://13.206.210.64:8000/api";
const currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });

async function api(path, { token, ...options } = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || "CartLabs request failed");
  return payload;
}

function App() {
  const [session, setSession] = useState(() => JSON.parse(localStorage.getItem("cartlabs.session") || "null"));
  const [view, setView] = useState("products");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [cart, setCart] = useState({ items: [], subtotal: 0, count: 0 });
  const [lastOrder, setLastOrder] = useState(null);

  useEffect(() => {
    if (session) localStorage.setItem("cartlabs.session", JSON.stringify(session));
    else localStorage.removeItem("cartlabs.session");
  }, [session]);

  async function refreshCart() {
    if (!session?.token) return;
    setCart(await api("/cart", { token: session.token }));
  }

  useEffect(() => {
    refreshCart().catch(() => {});
  }, [session?.token]);

  if (!session) {
    return <AuthShell onSession={setSession} />;
  }

  return (
    <div className="min-h-screen bg-ink text-white">
      <Navbar
        user={session.user}
        cartCount={cart.count}
        view={view}
        onNavigate={setView}
        onLogout={() => setSession(null)}
      />
      <main className="mx-auto max-w-7xl px-4 pb-16 pt-6 sm:px-6 lg:px-8">
        {view === "products" && (
          <ProductsPage
            token={session.token}
            onOpen={(product) => {
              setSelectedProduct(product);
              setView("detail");
            }}
            onAdd={async (product) => {
              const next = await api("/cart", {
                token: session.token,
                method: "POST",
                body: JSON.stringify({ productId: product.id, name: product.name, image: product.image, price: product.price, quantity: 1 }),
              });
              setCart(next);
            }}
          />
        )}
        {view === "detail" && selectedProduct && (
          <ProductDetail
            product={selectedProduct}
            token={session.token}
            onBack={() => setView("products")}
            onOpen={(product) => setSelectedProduct(product)}
            onAdd={async (product) => {
              const next = await api("/cart", {
                token: session.token,
                method: "POST",
                body: JSON.stringify({ productId: product.id, name: product.name, image: product.image, price: product.price, quantity: 1 }),
              });
              setCart(next);
            }}
          />
        )}
        {view === "cart" && <CartPage cart={cart} token={session.token} onRefresh={refreshCart} onCheckout={() => setView("checkout")} />}
        {view === "checkout" && (
          <CheckoutPage
            cart={cart}
            token={session.token}
            user={session.user}
            onPlaced={async (order) => {
              setLastOrder(order);
              await api("/cart/clear", { token: session.token, method: "POST" });
              await refreshCart();
              setView("tracking");
            }}
          />
        )}
        {view === "tracking" && <TrackingPage token={session.token} order={lastOrder} />}
      </main>
    </div>
  );
}

function AuthShell({ onSession }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ fullName: "", email: "", password: "" });
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const payload = await api(mode === "login" ? "/auth/login" : "/auth/register", {
        method: "POST",
        body: JSON.stringify(form),
      });
      onSession(payload);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="grid min-h-screen bg-ink text-white lg:grid-cols-[0.95fr_1.05fr]">
      <section className="relative hidden overflow-hidden border-r border-line bg-[radial-gradient(circle_at_25%_15%,rgba(49,214,164,.28),transparent_34%),linear-gradient(145deg,#10151d,#0d1117)] p-12 lg:block">
        <div className="absolute inset-x-12 bottom-12 rounded-lg border border-white/10 bg-white/[.04] p-6 shadow-glow backdrop-blur">
          <div className="mb-6 flex items-center gap-3">
            <div className="grid size-12 place-items-center rounded-md bg-mint text-ink">
              <ShoppingBag />
            </div>
            <div>
              <p className="text-3xl font-semibold">CartLabs</p>
              <p className="text-sm text-steel">Microservice commerce cockpit</p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 text-sm text-steel">
            {["JWT Auth", "Smart Catalog", "Order Tracking"].map((item) => (
              <div className="rounded-md border border-white/10 bg-black/20 p-4" key={item}>{item}</div>
            ))}
          </div>
        </div>
      </section>
      <section className="flex items-center justify-center px-5 py-12">
        <form onSubmit={submit} className="w-full max-w-md rounded-lg border border-line bg-panel p-6 shadow-2xl">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.18em] text-mint">Secure access</p>
              <h1 className="mt-2 text-3xl font-semibold">{mode === "login" ? "Log in to CartLabs" : "Create your account"}</h1>
            </div>
            {mode === "login" ? <ShieldCheck className="text-mint" /> : <UserPlus className="text-mint" />}
          </div>
          {mode === "register" && <TextField label="Full name" value={form.fullName} onChange={(fullName) => setForm({ ...form, fullName })} />}
          <TextField label="Email" type="email" value={form.email} onChange={(email) => setForm({ ...form, email })} />
          <TextField label="Password" type="password" value={form.password} onChange={(password) => setForm({ ...form, password })} />
          {error && <p className="mb-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">{error}</p>}
          <button className="flex w-full items-center justify-center gap-2 rounded-md bg-mint px-4 py-3 font-semibold text-ink transition hover:brightness-110">
            {mode === "login" ? <ShieldCheck size={18} /> : <UserPlus size={18} />}
            {mode === "login" ? "Login" : "Register"}
          </button>
          <button type="button" onClick={() => setMode(mode === "login" ? "register" : "login")} className="mt-4 w-full text-sm text-steel hover:text-white">
            {mode === "login" ? "No account yet? Register" : "Already registered? Login"}
          </button>
        </form>
      </section>
    </div>
  );
}

function Navbar({ user, cartCount, view, onNavigate, onLogout }) {
  const items = [
    ["products", "Products", Boxes],
    ["cart", "Cart", ShoppingCart],
    ["checkout", "Billing", CreditCard],
    ["tracking", "Tracking", Truck],
  ];
  const NavItems = ({ mobile = false }) => (
    <nav className={mobile ? "fixed inset-x-0 bottom-0 z-40 grid grid-cols-4 border-t border-line bg-ink/95 px-2 py-2 backdrop-blur md:hidden" : "hidden items-center gap-1 md:flex"}>
      {items.map(([key, label, Icon]) => (
        <button key={key} onClick={() => onNavigate(key)} className={`nav-btn ${mobile ? "h-12 justify-center px-2" : ""} ${view === key ? "nav-btn-active" : ""}`}>
          <Icon size={17} />
          <span className={mobile ? "sr-only" : ""}>{label}</span>
          {key === "cart" && cartCount > 0 ? <span className="badge">{cartCount}</span> : null}
        </button>
      ))}
    </nav>
  );

  return (
    <header className="sticky top-0 z-30 border-b border-line bg-ink/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <button onClick={() => onNavigate("products")} className="flex items-center gap-3">
          <span className="grid size-10 place-items-center rounded-md bg-mint text-ink"><ShoppingBag size={21} /></span>
          <span className="text-xl font-semibold">CartLabs</span>
        </button>
        <NavItems />
        <div className="flex items-center gap-3">
          <span className="hidden text-sm text-steel sm:inline">{user.fullName}</span>
          <button title="Logout" onClick={onLogout} className="icon-btn"><LogOut size={18} /></button>
        </div>
      </div>
      <NavItems mobile />
    </header>
  );
}

function ProductsPage({ token, onOpen, onAdd }) {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");

  useEffect(() => {
    const timer = setTimeout(async () => {
      const params = new URLSearchParams({ q: query, category });
      const payload = await api(`/products?${params}`, { token });
      setProducts(payload.products);
      setCategories(payload.categories);
    }, 180);
    return () => clearTimeout(timer);
  }, [query, category, token]);

  return (
    <>
      <section className="mb-8 grid gap-6 lg:grid-cols-[1fr_360px]">
        <div>
          <p className="text-sm uppercase tracking-[0.18em] text-mint">Commerce inventory</p>
          <h1 className="mt-3 max-w-3xl text-4xl font-semibold leading-tight sm:text-5xl">Production-grade shopping flow for curated tech products.</h1>
        </div>
        <div className="rounded-lg border border-line bg-panel p-4">
          <div className="mb-3 flex items-center gap-2 text-steel"><Sparkles size={18} /> Live catalog controls</div>
          <div className="relative">
            <Search className="absolute left-3 top-3 text-steel" size={18} />
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search products" className="input pl-10" />
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            {["all", ...categories].map((item) => (
              <button key={item} onClick={() => setCategory(item)} className={`chip ${category === item ? "chip-active" : ""}`}>{item}</button>
            ))}
          </div>
        </div>
      </section>
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {products.map((product) => <ProductCard key={product.id} product={product} onOpen={onOpen} onAdd={onAdd} />)}
      </section>
    </>
  );
}

function ProductCard({ product, onOpen, onAdd }) {
  return (
    <article className="group overflow-hidden rounded-lg border border-line bg-panel">
      <button onClick={() => onOpen(product)} className="block w-full text-left">
        <img src={product.image} alt={product.name} className="h-56 w-full object-cover transition duration-500 group-hover:scale-105" />
        <div className="p-5">
          <div className="mb-3 flex items-center justify-between text-sm text-steel">
            <span>{product.category}</span>
            <span>{product.rating} rating</span>
          </div>
          <h2 className="text-xl font-semibold">{product.name}</h2>
          <p className="mt-2 line-clamp-2 text-sm text-steel">{product.description}</p>
        </div>
      </button>
      <div className="flex items-center justify-between border-t border-line p-5">
        <span className="text-2xl font-semibold">{currency.format(product.price)}</span>
        <button onClick={() => onAdd(product)} className="primary-btn"><ShoppingCart size={17} /> Add</button>
      </div>
    </article>
  );
}

function ProductDetail({ product, token, onBack, onOpen, onAdd }) {
  const [recommendations, setRecommendations] = useState([]);
  useEffect(() => {
    api(`/recommendations/${product.id}`, { token }).then((payload) => setRecommendations(payload.recommendations));
  }, [product.id, token]);

  return (
    <div>
      <button onClick={onBack} className="mb-5 flex items-center gap-2 text-sm text-steel hover:text-white"><ArrowLeft size={17} /> Back to products</button>
      <section className="grid gap-8 lg:grid-cols-[1fr_0.8fr]">
        <img src={product.image} alt={product.name} className="h-[520px] w-full rounded-lg object-cover" />
        <div>
          <p className="text-sm uppercase tracking-[0.18em] text-mint">{product.category}</p>
          <h1 className="mt-3 text-4xl font-semibold">{product.name}</h1>
          <p className="mt-5 text-lg leading-8 text-steel">{product.description}</p>
          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {product.features?.map((feature) => <div key={feature} className="flex items-center gap-2 rounded-md border border-line bg-panel p-3 text-sm"><BadgeCheck className="text-mint" size={18} /> {feature}</div>)}
          </div>
          <div className="mt-8 flex items-center justify-between rounded-lg border border-line bg-panel p-5">
            <span className="text-3xl font-semibold">{currency.format(product.price)}</span>
            <button onClick={() => onAdd(product)} className="primary-btn px-5 py-3"><ShoppingCart size={18} /> Add to cart</button>
          </div>
        </div>
      </section>
      <section className="mt-10">
        <h2 className="mb-4 text-2xl font-semibold">Recommended with this product</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {recommendations.map((item) => <ProductCard key={item.id} product={item} onOpen={onOpen} onAdd={onAdd} />)}
        </div>
      </section>
    </div>
  );
}

function CartPage({ cart, token, onRefresh, onCheckout }) {
  async function remove(productId) {
    await api(`/cart/${productId}`, { token, method: "DELETE" });
    await onRefresh();
  }
  return (
    <section>
      <h1 className="mb-6 text-4xl font-semibold">Cart</h1>
      <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
        <div className="space-y-3">
          {cart.items.map((item) => (
            <div key={item.productId} className="flex gap-4 rounded-lg border border-line bg-panel p-4">
              <img src={item.image} alt={item.name} className="size-24 rounded-md object-cover" />
              <div className="min-w-0 flex-1">
                <h2 className="font-semibold">{item.name}</h2>
                <p className="text-sm text-steel">Qty {item.quantity}</p>
                <p className="mt-3 text-lg font-semibold">{currency.format(item.lineTotal)}</p>
              </div>
              <button onClick={() => remove(item.productId)} className="text-sm text-steel hover:text-white">Remove</button>
            </div>
          ))}
          {cart.items.length === 0 && <EmptyState title="Your cart is empty" />}
        </div>
        <Summary subtotal={cart.subtotal} disabled={!cart.items.length} onCheckout={onCheckout} ctaLabel="Continue to billing" />
      </div>
    </section>
  );
}

function Summary({ subtotal, disabled, onCheckout, ctaLabel = "Continue" }) {
  return (
    <aside className="h-fit rounded-lg border border-line bg-panel p-5">
      <h2 className="mb-4 text-xl font-semibold">Order summary</h2>
      <div className="space-y-3 text-sm text-steel">
        <div className="flex justify-between"><span>Subtotal</span><span>{currency.format(subtotal)}</span></div>
        <div className="flex justify-between"><span>Shipping</span><span>Calculated later</span></div>
        <div className="flex justify-between"><span>Payment</span><span>Coming later</span></div>
      </div>
      <div className="my-5 border-t border-line" />
      <div className="flex justify-between text-xl font-semibold"><span>Total</span><span>{currency.format(subtotal)}</span></div>
      <button disabled={disabled} onClick={onCheckout} className="primary-btn mt-5 w-full justify-center py-3 disabled:cursor-not-allowed disabled:opacity-40"><CreditCard size={18} /> {ctaLabel}</button>
    </aside>
  );
}

function CheckoutPage({ cart, token, user, onPlaced }) {
  const [shipping, setShipping] = useState({ fullName: user.fullName, email: user.email, phone: "", address: "", city: "", postalCode: "" });
  const [error, setError] = useState("");
  async function placeOrder(event) {
    event.preventDefault();
    setError("");
    try {
      const payload = await api("/orders", { token, method: "POST", body: JSON.stringify({ shipping, items: cart.items }) });
      await onPlaced(payload.order);
    } catch (err) {
      setError(err.message);
    }
  }
  return (
    <section className="grid gap-6 lg:grid-cols-[1fr_340px]">
      <form onSubmit={placeOrder} className="rounded-lg border border-line bg-panel p-5">
        <h1 className="mb-5 text-3xl font-semibold">Billing and delivery details</h1>
        <div className="grid gap-4 sm:grid-cols-2">
          {[
            ["fullName", "Full name"],
            ["email", "Email"],
            ["phone", "Phone"],
            ["city", "City"],
            ["postalCode", "Postal code"],
          ].map(([key, label]) => <TextField key={key} label={label} value={shipping[key]} onChange={(value) => setShipping({ ...shipping, [key]: value })} />)}
        </div>
        <label className="mt-4 block text-sm text-steel">Address<textarea value={shipping.address} onChange={(event) => setShipping({ ...shipping, address: event.target.value })} className="input mt-2 min-h-28" /></label>
        {error && <p className="mt-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">{error}</p>}
        <button className="primary-btn mt-5 px-5 py-3"><PackageCheck size={18} /> Place order</button>
      </form>
      <Summary subtotal={cart.subtotal} disabled={!cart.items.length} onCheckout={placeOrder} ctaLabel="Place order" />
    </section>
  );
}

function TrackingPage({ token, order }) {
  const [tracking, setTracking] = useState(null);
  useEffect(() => {
    if (order?.id) api(`/tracking/${order.id}`, { token }).then(setTracking);
  }, [order?.id, token]);

  if (!order) return <EmptyState title="Place an order to start tracking" />;
  return (
    <section className="rounded-lg border border-line bg-panel p-6">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.18em] text-mint">Order #{order.id}</p>
          <h1 className="mt-2 text-3xl font-semibold">Tracking timeline</h1>
        </div>
        <div className="rounded-md border border-line px-4 py-3 text-sm text-steel">{tracking?.carrier} · ETA {tracking?.eta}</div>
      </div>
      <div className="space-y-4">
        {tracking?.steps.map((step) => (
          <div key={step.label} className="flex gap-4 rounded-md border border-line bg-ink/40 p-4">
            <span className={`grid size-9 shrink-0 place-items-center rounded-full ${step.state === "pending" ? "bg-line text-steel" : "bg-mint text-ink"}`}>
              {step.state === "pending" ? <Truck size={17} /> : <Check size={17} />}
            </span>
            <div>
              <h2 className="font-semibold">{step.label}</h2>
              <p className="text-sm text-steel">{step.detail}</p>
              {step.timestamp && <p className="mt-1 text-xs text-steel">{new Date(step.timestamp).toLocaleString()}</p>}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function TextField({ label, value, onChange, type = "text" }) {
  return (
    <label className="mb-4 block text-sm text-steel">
      {label}
      <input type={type} value={value} onChange={(event) => onChange(event.target.value)} className="input mt-2" />
    </label>
  );
}

function EmptyState({ title }) {
  return <div className="rounded-lg border border-dashed border-line bg-panel p-10 text-center text-steel">{title}</div>;
}

createRoot(document.getElementById("root")).render(<App />);
