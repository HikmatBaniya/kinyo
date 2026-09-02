"""Content that was previously carried in tables, rewritten as headed prose with
bullet lists in the style of the sample proposal.

Each entry is (group heading, [bullet, ...]). The group heading is emitted as a
bold run-in line and the bullets beneath it.
"""

# --------------------------------------------- 2.2 study of related systems --
RELATED_SYSTEMS = [
    ("1) Shopify", [
        "Platform: hosted software as a service, reached through a web browser.",
        "Approach: a proprietary multi-tenant platform with a template language "
        "that sellers use to theme their storefronts.",
        "Strengths: self-service store creation, custom domain mapping, a mature "
        "checkout and a large application ecosystem.",
        "Limitations: the subscription is charged in foreign currency, the "
        "storefront logic cannot be modified, and there is no integration with "
        "local payment or delivery providers.",
    ]),
    ("2) WooCommerce", [
        "Platform: self-hosted, installed as a plugin into a WordPress site.",
        "Approach: extends a PHP and MySQL content management system with "
        "commerce features.",
        "Strengths: open source, no licence cost, a very large plugin catalogue "
        "and complete control of the storefront.",
        "Limitations: single tenant by design. Each seller needs a separate "
        "installation, database and hosting account, which is precisely the "
        "barrier this project removes.",
    ]),
    ("3) Adobe Commerce (Magento)", [
        "Platform: self-hosted or vendor-hosted, reached through a web browser.",
        "Approach: a modular PHP commerce framework with support for several "
        "storefronts from one installation.",
        "Strengths: rich catalogue, pricing and promotion rules, and genuine "
        "multi-store capability.",
        "Limitations: heavy hardware and expertise requirements, and its "
        "multi-store support assumes one owning business rather than unrelated "
        "tenants who must not see each other's data.",
    ]),
    ("4) Wix eCommerce", [
        "Platform: hosted software as a service.",
        "Approach: a proprietary multi-tenant website builder with a commerce "
        "module bolted on.",
        "Strengths: drag-and-drop storefront design, with hosting and domain "
        "management included.",
        "Limitations: the storefront structure is fixed by the builder, data "
        "export is limited, and the subscription is again priced in foreign "
        "currency.",
    ]),
    ("5) Saleor", [
        "Platform: self-hosted, deployed by the merchant or an integrator.",
        "Approach: a Python and Django core that exposes a GraphQL interface, "
        "with the storefront kept as a separate application.",
        "Strengths: a modern interface-first design, a strong catalogue and "
        "sales-channel model, and an open licence.",
        "Limitations: aimed at development teams. There is no self-service "
        "tenant onboarding, and a separate deployment is expected per merchant.",
    ]),
    ("6) Medusa", [
        "Platform: self-hosted, deployed by the merchant or an integrator.",
        "Approach: a Node.js commerce engine with a headless interface and a "
        "separate administration application.",
        "Strengths: modular services, an open licence, and a flexible order and "
        "pricing model.",
        "Limitations: single-merchant by default. Multi-tenancy has to be added "
        "by the integrator, and a developer is required to operate it.",
    ]),
]

# ------------------------------- 2.4 functional and non-functional needs ----
FUNCTIONAL_REQUIREMENTS = [
    ("1) Authentication and Access Control", [
        "Sellers, staff and platform administrators shall be able to register, "
        "log in and log out, with sessions carried by signed tokens.",
        "A store owner shall be able to invite staff and assign them roles, and "
        "each role shall permit only the operations defined for it.",
        "Storefront customers shall authenticate separately from platform users, "
        "because a customer account belongs to one store rather than to the "
        "platform.",
    ]),
    ("2) Store Provisioning and Domain Mapping", [
        "A registered seller shall be able to create a store, to which the "
        "system assigns a unique slug and a platform subdomain.",
        "A store owner shall be able to attach a custom domain, which the system "
        "verifies before serving the storefront from it.",
        "A platform administrator shall be able to approve, suspend and "
        "reinstate stores.",
    ]),
    ("3) Catalogue and Inventory Management", [
        "Sellers shall be able to create, update, publish and archive products, "
        "variants, collections and product media.",
        "Each variant shall carry its own stock keeping unit and price, and the "
        "system shall record stock on hand and reserved stock for each variant.",
        "The system shall prevent an order that requests more units than are "
        "available.",
    ]),
    ("4) Storefront and Shopping Cart", [
        "The system shall resolve the tenant from the request host and render "
        "only that tenant's catalogue and theme.",
        "Registered and guest customers shall be able to add, update and remove "
        "cart lines, and the cart shall persist between visits.",
        "The storefront shall support product search and browsing by collection.",
    ]),
    ("5) Checkout and Order Processing", [
        "Customers shall be able to place an order with a delivery address and a "
        "cash on delivery payment method, and shall receive an order number.",
        "The system shall recompute the subtotal, discount, shipping charge and "
        "total on the server at checkout rather than trusting values sent by the "
        "client.",
        "Store staff shall be able to advance an order through its status "
        "sequence and record collection of payment on delivery.",
    ]),
    ("6) Discounts, Shipping and Reporting", [
        "Sellers shall be able to define discount codes with validity periods "
        "and minimum order values, and shipping zones with associated rates.",
        "The system shall generate sales and inventory reports for a store on "
        "demand, and a platform activity summary for administrators.",
    ]),
    ("7) Error Handling and Validation", [
        "Invalid input shall be rejected with a clear, non-technical message "
        "identifying the field at fault.",
        "A request for a host that does not map to an active store shall return "
        "a store-not-found page rather than an application error.",
        "If stock changes between adding an item to the cart and confirming the "
        "order, the customer shall be returned to the cart with the affected "
        "lines identified.",
    ]),
]

NONFUNCTIONAL_REQUIREMENTS = [
    ("1) Tenant Isolation", [
        "No request authenticated for one tenant shall be able to read or modify "
        "data belonging to another tenant.",
        "Isolation shall be enforced in a single data-access layer and "
        "reinforced by row-level security policies in the database.",
    ]),
    ("2) Security", [
        "Credentials shall be stored only as salted hashes using Argon2, and all "
        "traffic shall be served over HTTPS.",
        "The application shall address the OWASP Top 10 categories, in "
        "particular broken access control and identification failures.",
        "No card or bank data is collected or stored, because no online payment "
        "gateway is integrated.",
    ]),
    ("3) Performance", [
        "A storefront catalogue page shall be returned within 3 seconds under "
        "the documented test conditions.",
        "Storefront responses shall be cached so that repeated catalogue reads "
        "do not reach the database on every request.",
    ]),
    ("4) Usability", [
        "A seller shall be able to create a store and publish a first product "
        "without training or developer assistance.",
        "The storefront shall be responsive and usable on a mobile browser.",
    ]),
    ("5) Scalability", [
        "Adding a further seller shall require no additional deployment, "
        "database or hosting account.",
        "The application tier shall be stateless so that further instances can "
        "be added behind a load balancer.",
    ]),
    ("6) Maintainability", [
        "Code shall be modular, documented and version-controlled in a Git "
        "repository.",
        "Database changes shall be applied through versioned migrations "
        "committed alongside the code that requires them.",
    ]),
]

# ------------------------------------------------------ 2.5 feasibility ----
FEASIBILITY = [
    ("1) Technical Feasibility", [
        "Every required technology is mature, openly licensed and "
        "comprehensively documented: FastAPI for the application tier, Next.js "
        "for the presentation tier, PostgreSQL for storage, and SQLAlchemy with "
        "Alembic for data access and migrations.",
        "The team already has working knowledge of Python, JavaScript and "
        "relational databases.",
        "A standard laptop with 8 GB of memory is sufficient for development, "
        "because the workload is dominated by database access rather than "
        "computation. No specialised hardware is required.",
        "The shared-database multi-tenant pattern adopted is well described in "
        "the literature, so the highest-risk part of the design is not being "
        "invented from scratch.",
    ]),
    ("2) Operational Feasibility", [
        "The intended users already sell online through social media, so the "
        "concepts of a catalogue, an order and a delivery address are familiar.",
        "The seller dashboard replaces a manual notebook rather than an existing "
        "software system, which removes the migration effort that normally "
        "blocks adoption.",
        "Store provisioning is self-service, so a seller can open a store from a "
        "registration form without contacting the platform operator.",
        "Cash on delivery is retained as the settlement method because it is "
        "what these sellers and their customers already use.",
    ]),
    ("3) Economic Feasibility", [
        "Every tool in the stack is free and open source, and no commercial "
        "licence is required at any stage.",
        "Development and demonstration hosting are covered by free tiers for the "
        "application and a small managed PostgreSQL instance.",
        "The only unavoidable cost is a domain name for the demonstration "
        "deployment, which is a small annual fee.",
        "For the platform operator, the shared-database design means the "
        "marginal cost of an additional seller is the cost of the rows that "
        "seller creates, rather than the cost of a further deployment.",
    ]),
    ("4) Schedule Feasibility", [
        "The project is scheduled over six months, as set out in Section 3.2.",
        "Requirement analysis, design, development, integration, testing, "
        "deployment and documentation are treated as separate activities, and "
        "testing is allocated its own period rather than being absorbed into "
        "development.",
        "Tenant isolation, the highest-risk element of the design, is built in "
        "the first development iteration so that it is exercised by every later "
        "increment.",
    ]),
    ("5) Legal and Ethical Feasibility", [
        "The system stores personal data of storefront customers, namely name, "
        "contact details and delivery address. That data is collected only for "
        "order fulfilment, is scoped to the tenant that collected it, and is "
        "transmitted over HTTPS.",
        "No card or bank data is collected or stored, because no online payment "
        "gateway is integrated, which keeps the project outside the scope of "
        "payment card compliance.",
        "All third-party libraries used are released under permissive "
        "open-source licences that allow academic and commercial use.",
    ]),
]

# ----------------------------------------- 4.1 hardware and software needs --
HARDWARE_REQUIREMENTS = [
    ("1) Processor", [
        "Minimum: Intel Core i5 (8th generation) or an equivalent AMD Ryzen 5. "
        "Sufficient for running the application server, the database and the "
        "front-end build together.",
        "Recommended: Intel Core i7 or Ryzen 7, which shortens front-end build "
        "times and makes running the full stack in containers comfortable.",
    ]),
    ("2) Memory", [
        "Minimum: 8 GB. Enough to run PostgreSQL, Redis, the FastAPI service and "
        "the Next.js development server at the same time.",
        "Recommended: 16 GB, which leaves room for the browser, the editor and "
        "the container runtime without swapping.",
    ]),
    ("3) Storage", [
        "A solid state drive is recommended, because dependency installation and "
        "front-end builds are dominated by small-file input and output.",
        "Minimum 40 GB free for source code, dependencies, container images and "
        "the local database.",
    ]),
    ("4) Display and Network", [
        "A display of 1920 by 1080 or higher, which makes dashboard and "
        "storefront layout work practical.",
        "A broadband internet connection for package installation, deployment "
        "and domain verification.",
    ]),
    ("5) Deployment Server", [
        "One application instance of 1 virtual CPU and 1 GB of memory, which is "
        "within the free tier of the hosting platforms considered.",
        "A small managed PostgreSQL instance for the shared database.",
        "No graphics processor is required at any stage, because the system "
        "performs no model training or heavy computation.",
    ]),
]

SOFTWARE_REQUIREMENTS = [
    ("1) Operating System", [
        "Any modern 64-bit operating system. Windows 10 or 11, or Ubuntu 22.04 "
        "LTS, are used by the team and are both supported by every tool in the "
        "stack.",
    ]),
    ("2) Back End", [
        "Python 3.11 as the implementation language.",
        "FastAPI with Pydantic and Uvicorn for the REST interface, request "
        "validation and generated interface documentation.",
        "SQLAlchemy 2.0 for object-relational mapping, which is where the tenant "
        "scoping is applied, and Alembic for versioned schema migrations.",
    ]),
    ("3) Front End", [
        "TypeScript as the implementation language.",
        "Next.js 15 with React for server-rendered storefronts, the seller "
        "dashboard and the platform administration console.",
        "Tailwind CSS for styling, which keeps the storefront themes to a small "
        "set of design tokens.",
    ]),
    ("4) Data and Storage", [
        "PostgreSQL 16 as the relational database, chosen for its row-level "
        "security policies and JSONB columns.",
        "Redis 7 for cached storefront responses and session data.",
        "An S3-compatible object store for product images and theme assets.",
    ]),
    ("5) Development and Testing Tools", [
        "Visual Studio Code as the development environment.",
        "Docker and Docker Compose for a reproducible local database and cache.",
        "pytest for unit and integration testing, and Playwright for end-to-end "
        "tests through a real browser.",
        "Git and GitHub for source control and collaboration.",
    ]),
]

# ---------------------------------------------- 4.2 proposed technology stack --
TECHNOLOGY_STACK = [
    ("1) Presentation Tier", [
        "Next.js 15 with React and Tailwind CSS, served over HTTPS.",
        "Chosen because its middleware runs before routing and can rewrite a "
        "request based on the Host header, which is exactly the mechanism "
        "required to serve many storefronts and two applications from one "
        "deployment, and because server-side rendering produces complete HTML "
        "for storefront pages so that they are indexable by search engines.",
    ]),
    ("2) Application Tier", [
        "FastAPI with Pydantic and Uvicorn, exposing a versioned REST interface.",
        "Chosen because it validates every request and response against declared "
        "models and generates interface documentation from those same models, so "
        "the contract cannot drift from the code. Its asynchronous request "
        "handling also suits a workload dominated by database waits. Django was "
        "considered but its session-based, single-tenant conventions would have "
        "to be worked against rather than with.",
    ]),
    ("3) Data Tier", [
        "PostgreSQL 16 as the single shared database, with Redis 7 for caching "
        "and an S3-compatible object store for media.",
        "PostgreSQL was chosen over MySQL because the tenancy design depends on "
        "features it provides directly: row-level security policies give a "
        "database-level guarantee of isolation behind the application filter, "
        "and JSONB columns hold variant options and theme settings without a "
        "separate table for every attribute.",
    ]),
    ("4) Data Access", [
        "SQLAlchemy 2.0 with Alembic migrations.",
        "Chosen because the tenant filter can be implemented once, in the "
        "session and query layer, and applied to every tenant-owned model rather "
        "than repeated in each query. Alembic keeps the schema under version "
        "control alongside the code.",
    ]),
    ("5) Authentication", [
        "JSON Web Tokens for session handling and Argon2 for password hashing.",
        "Argon2 was chosen over older algorithms because it is the current "
        "recommendation for password storage in the OWASP guidance.",
    ]),
    ("6) Deployment", [
        "Vercel for the presentation tier and Render for the application tier "
        "and the managed database.",
        "Both offer free tiers sufficient for a demonstration deployment, and "
        "both support the custom domain mapping the storefronts require.",
    ]),
]
