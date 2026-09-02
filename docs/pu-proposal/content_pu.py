"""Content for the Kinyo project proposal, in the Purbanchal University /
Himalayan Whitehouse International College format.

Placeholders in square brackets must be replaced before submission.
"""

META = {
    "university": "PURBANCHAL UNIVERSITY",
    "college": "HIMALAYAN WHITEHOUSE INTERNATIONAL COLLEGE",
    "college_address": "PUTALISADAK, KATHMANDU",
    "title": "“Kinyo: A Multi-Tenant E-Commerce Platform for Independent "
             "Sellers”",
    "students": [
        ("Hikmat Baniya", "15"),
        ("Nishan Neupane", "23"),
    ],
    "semester_line": "8th Semester Apprenticeship Project",
    "date": "September 2026",
    "city": "Kathmandu, Nepal",
    "repo": "[https://github.com/<your-username>/kinyo]",
}

ABSTRACT = [
    "Kinyo is a multi-tenant e-commerce platform that allows many independent sellers to "
    "create, customise and operate their own branded online storefronts from a single "
    "deployed application. Most small retailers in Nepal sell online through social media "
    "pages and messaging applications, where the catalogue is a series of image posts, the "
    "order book is a chat thread and stock is tracked from memory. Existing hosted "
    "platforms solve this but charge subscriptions in foreign currency, while existing "
    "open-source platforms are built around one merchant per deployment and require a "
    "developer to install and maintain.",

    "The proposed system is built as a three-tier web application. A FastAPI service "
    "exposes a versioned REST interface over a single PostgreSQL database in which every "
    "tenant-owned table carries a tenant identifier, and a Next.js application resolves "
    "the store from the HTTP Host header so that storefronts are reachable both at a "
    "platform subdomain and at a custom domain owned by the seller. Isolation between "
    "tenants is enforced in one data-access layer and backed by row-level security in the "
    "database, and is verified by a dedicated group of cross-tenant test cases rather than "
    "assumed. The platform covers store provisioning, domain mapping, storefront themes, "
    "the product catalogue with variants and collections, variant-level inventory, cart, "
    "checkout, the order lifecycle, discounts, shipping zones, sales reporting and a "
    "platform administration console. Orders are settled by cash on delivery; online "
    "payment gateway integration is outside the scope of this project.",

    "Keywords: Multi-Tenant Architecture, E-Commerce Platform, Software as a Service, "
    "FastAPI, Next.js, PostgreSQL, Tenant Isolation, Storefront Routing, Inventory "
    "Management, Cash on Delivery.",
]

ABBREVIATIONS = [
    ("API", "Application Programming Interface"),
    ("BIT", "Bachelor of Information Technology"),
    ("CDN", "Content Delivery Network"),
    ("CNAME", "Canonical Name (DNS record)"),
    ("COD", "Cash on Delivery"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("CSS", "Cascading Style Sheets"),
    ("CSV", "Comma-Separated Values"),
    ("DFD", "Data Flow Diagram"),
    ("DNS", "Domain Name System"),
    ("ERD", "Entity Relationship Diagram"),
    ("FK", "Foreign Key"),
    ("GB", "Gigabyte"),
    ("HTML", "HyperText Markup Language"),
    ("HTTP", "HyperText Transfer Protocol"),
    ("HTTPS", "HyperText Transfer Protocol Secure"),
    ("IDE", "Integrated Development Environment"),
    ("JSON", "JavaScript Object Notation"),
    ("JWT", "JSON Web Token"),
    ("KPI", "Key Performance Indicator"),
    ("ORM", "Object-Relational Mapping"),
    ("OS", "Operating System"),
    ("OWASP", "Open Web Application Security Project"),
    ("PK", "Primary Key"),
    ("RAM", "Random Access Memory"),
    ("RBAC", "Role-Based Access Control"),
    ("RDBMS", "Relational Database Management System"),
    ("REST", "Representational State Transfer"),
    ("RLS", "Row-Level Security"),
    ("SaaS", "Software as a Service"),
    ("SDLC", "Software Development Life Cycle"),
    ("SEO", "Search Engine Optimisation"),
    ("SKU", "Stock Keeping Unit"),
    ("SME", "Small and Medium Enterprise"),
    ("SQL", "Structured Query Language"),
    ("SSD", "Solid State Drive"),
    ("SSR", "Server-Side Rendering"),
    ("UAT", "User Acceptance Testing"),
    ("UI", "User Interface"),
    ("UML", "Unified Modeling Language"),
    ("URL", "Uniform Resource Locator"),
    ("UUID", "Universally Unique Identifier"),
    ("UX", "User Experience"),
    ("VS Code", "Visual Studio Code"),
]

FIGURES = {
    1: ("SDLC Model", "fig1_sdlc.png", 6.0),
    2: ("System Architecture", "fig2_architecture.png", 5.9),
    3: ("System Flowchart", "fig3_flowchart.png", 5.6),
    4: ("Context Diagram", "fig4_usecase.png", 5.9),   # replaced in build order below
    5: ("Level 1 DFD", "fig6_dfd1.png", 5.9),
    6: ("Use Case Diagram", "fig4_usecase.png", 5.8),
    7: ("ER Diagram", "fig7_erd.png", 6.0),
    8: ("Gantt Chart", "fig8_gantt.png", 6.0),
}
# Figure 4 is the context diagram; corrected here so the mapping stays explicit.
FIGURES[4] = ("Context Diagram", "fig5_dfd0.png", 6.0)

TABLE_TITLES = {
    1: "Comparison of Existing E-Commerce Platforms",
    2: "Hardware Requirements",
    3: "Software Requirements",
    4: "Evaluation Summary Table",
}

# ============================================================ CHAPTER 1 =====
CH1_INTRO = [
    "Retail trade in Nepal is dominated by small and medium enterprises that operate from "
    "a single shop and sell to a local customer base. Over the past decade a large share "
    "of these sellers has moved part of that trade online, but the move has been made "
    "almost entirely through general-purpose social media pages and messaging "
    "applications rather than through sales channels the seller owns. A seller typically "
    "publishes product photographs on a social media page, negotiates price and "
    "availability in private messages, records the resulting orders in a notebook or a "
    "spreadsheet, and arranges delivery by telephone. Commercial guidance published for "
    "Nepal notes that online retail is expanding quickly while the supporting commercial "
    "infrastructure remains uneven [16].",

    "This project proposes Kinyo, a multi-tenant e-commerce platform on which many "
    "independent sellers operate their own branded storefronts from a single deployed "
    "application. Multi-tenancy is the architectural practice of serving many customer "
    "organisations, called tenants, from one running instance of an application and one "
    "database, with the data of each tenant isolated from the others [1]. Applying that "
    "practice here allows the cost of hosting, maintenance and upgrades to be shared "
    "across all sellers, which is what makes an affordable, locally operated storefront "
    "service possible for a business that could not fund a website of its own.",

    "The platform is built entirely on open-source technology. The application tier is a "
    "FastAPI service exposing a REST interface [7], the presentation tier is a Next.js "
    "application that renders public storefronts on the server for search engine "
    "visibility [8], and the data tier is a single PostgreSQL database in which every "
    "tenant-owned table carries a tenant identifier [9]. A seller registers, creates a "
    "store, publishes a catalogue and begins receiving orders without installing "
    "anything, obtaining hosting, or writing code. This makes the project both an "
    "academic exercise in multi-tenant system design and a deployable tool that a real "
    "Nepali retailer can use.",
]

CH1_PROBLEM_INTRO = [
    "Independent retailers in Nepal who wish to sell online have no affordable way to "
    "obtain and operate a storefront that they control. The current process depends on "
    "social media pages and manual record keeping, which is slow, error-prone and gives "
    "the seller no reliable record of what was sold, to whom, or at what price.",

    "The parties that bear the cost are the sellers, who lose sales and spend unpaid hours "
    "on manual coordination, and their customers, who cannot see accurate availability or "
    "check the status of an order. The specific problems identified are the following:",
]

CH1_PROBLEM_POINTS = [
    "Catalogue management is manual. Products live as image posts, so prices, variants "
    "and availability cannot be updated reliably or searched.",
    "There is no stock control. Items are frequently sold after they are already out of "
    "stock, and the seller only discovers this when attempting to dispatch the goods.",
    "Orders are recorded in chat threads and notebooks, so they are duplicated, lost, or "
    "impossible to trace once the conversation scrolls away.",
    "Pricing, discounts and delivery charges are re-negotiated with every customer, which "
    "is inconsistent and time-consuming.",
    "The seller has no branded web presence, cannot be found through ordinary web search, "
    "and cannot export a customer list from a platform they do not own.",
    "Hosted platforms such as Shopify and Wix charge recurring subscriptions in foreign "
    "currency, which places them beyond the reach of a single-shop retailer.",
    "Open-source platforms such as WooCommerce, Saleor and Medusa are free of licence "
    "cost but assume one deployment per merchant and require a developer to install, host "
    "and maintain them.",
]

CH1_GENERAL_OBJECTIVE = (
    "To design, develop and deploy a multi-tenant e-commerce platform that enables "
    "independent sellers to create, customise and operate their own branded online "
    "storefronts from a single shared application."
)

CH1_SPECIFIC_OBJECTIVES = [
    "To analyse the requirements of independent sellers and their customers for online "
    "catalogue management, storefront presentation and order handling.",
    "To design a shared-database multi-tenant data model and a three-tier architecture in "
    "which every tenant-owned record is isolated by a tenant identifier.",
    "To implement the store provisioning, catalogue, cart and order modules together with "
    "host-based storefront routing, and to verify them against 40 defined test cases "
    "covering functional behaviour and cross-tenant data isolation.",
    "To deploy the platform as a web application serving seller dashboards and customer "
    "storefronts over subdomain and custom-domain addresses.",
]

CH1_SCOPE_INTRO = [
    "The system is a storefront and order-management platform. It is not an accounting "
    "system, a marketplace, or a logistics system. The scope includes complete source "
    "code and documentation hosted in a public Git repository, and excludes online "
    "payment gateway integration, mobile application development, accounting and tax "
    "filing, warehouse and courier dispatch management, and multi-currency pricing. "
    "Orders are settled by cash on delivery and the payment status is recorded manually "
    "by the seller. The platform includes:",
]

CH1_SCOPE_POINTS = [
    "Seller registration, role-based staff access and store provisioning",
    "Subdomain allocation and verified custom domain mapping",
    "Storefront theme selection and customisation",
    "Product catalogue with variants, collections and media",
    "Variant-level inventory tracking with stock reservation",
    "Shopping cart for both registered and guest customers",
    "Checkout, order placement and order lifecycle tracking",
    "Discount codes, shipping zones and shipping rates",
    "Sales and inventory reporting for sellers",
    "A platform administration console for approving and suspending stores",
]

CH1_SIGNIFICANCE = [
    "Gives Nepali retailers a branded storefront they own, at a cost a single-shop "
    "business can sustain, instead of a page inside someone else's platform.",
    "Replaces the manual order book with a recorded order lifecycle, removing the "
    "duplication and loss of orders caused by tracking sales in chat threads.",
    "Prevents overselling by reserving stock inside the same transaction that creates the "
    "order.",
    "Makes products discoverable through ordinary web search, because storefront pages are "
    "rendered on the server and served from a domain the seller controls.",
    "Produces a documented reference implementation of shared-schema multi-tenancy in a "
    "Python and TypeScript stack, reusable by later academic projects.",
]

CH1_LIMITATION = [
    "No online payment gateway is integrated; all orders are settled by cash on delivery.",
    "The platform is web-only; no native mobile application is produced, although the "
    "storefronts are responsive and usable on mobile browsers.",
    "Only physical goods are supported. Digital products, subscriptions and services are "
    "not modelled.",
    "Each store operates in a single currency, set at the tenant level.",
    "Custom domains require the seller to configure a DNS record with their own registrar, "
    "which the platform can verify but cannot perform on the seller's behalf.",
    "Free hosting tiers used for the demonstration deployment impose cold-start delays and "
    "limits on concurrent traffic.",
]

# ============================================================ CHAPTER 2 =====
CH2_RESEARCH = [
    "Multi-tenant software architecture has been studied extensively since hosted business "
    "applications became common. Chong and Carraro [1] distinguish three approaches to "
    "isolating tenant data: a separate database for each tenant, a shared database with a "
    "separate schema for each tenant, and a shared database with a shared schema in which "
    "every tenant-owned row carries a tenant identifier. The three approaches trade "
    "isolation against operating cost, with separate databases giving the strongest "
    "isolation at the highest per-tenant cost and the shared schema giving the lowest cost "
    "while requiring the application itself to enforce isolation on every query.",

    "Krebs, Momm and Kounev [3] reach a compatible conclusion from a performance and "
    "resource-sharing standpoint, and report that the shared-schema form is the only one "
    "that remains economical as the number of small tenants grows, because each additional "
    "tenant costs only the rows it creates rather than a further database instance. "
    "Bezemer and Zaidman [2] examine the maintenance consequences of the same design and "
    "observe that a single shared instance means a defect is fixed once for every tenant, "
    "but equally that a defect in the isolation logic is exposed to every tenant "
    "simultaneously. Their finding directly motivates the decision in this project to "
    "implement tenant scoping in one data-access layer and to test cross-tenant access "
    "explicitly rather than relying on each individual query being written correctly.",

    "On the commercial side, several mature platforms address parts of the same problem. "
    "Shopify [12] demonstrates that self-service tenant onboarding, custom domain mapping "
    "and themed storefronts can be delivered from a single hosted system, but its "
    "storefront logic is closed and its subscription is priced in foreign currency. "
    "WooCommerce [13] shows that an open, extensible commerce system can be assembled from "
    "a plugin architecture, but it is single-tenant: each seller needs a separate "
    "installation, database and hosting account. Saleor [14] and Medusa [15] represent the "
    "modern API-first generation of open-source commerce engines, with clean separation "
    "between the commerce API and the storefront, but both assume a single merchant per "
    "deployment and expect a development team to operate them.",

    "Table 1 compares these systems against the requirements of this project. The "
    "comparison shows a consistent gap: the systems that are genuinely multi-tenant are "
    "closed and subscription-priced, while the systems that are open and free of licence "
    "cost are single-tenant. No reviewed system combines self-service multi-tenancy with "
    "an open stack that a small Nepali retailer can be onboarded onto without a developer, "
    "which is the gap this project addresses.",
]

TABLE1_ROWS = [
    ("Shopify [12]", "Hosted SaaS", "Proprietary multi-tenant SaaS with a template "
     "language for themes", "Yes",
     "Subscription in foreign currency; storefront logic not modifiable"),
    ("WooCommerce [13]", "Self-hosted", "WordPress plugin over a PHP and MySQL stack",
     "No", "One installation, database and hosting account per seller"),
    ("Saleor [14]", "Self-hosted", "Python and Django core exposing a GraphQL API",
     "No", "Aimed at development teams; no self-service tenant onboarding"),
    ("Medusa [15]", "Self-hosted", "Node.js commerce engine with a headless API",
     "No", "Multi-tenancy must be added by the integrator"),
    ("Kinyo (proposed)", "Self-hosted", "FastAPI and Next.js over a shared PostgreSQL "
     "database with tenant_id scoping", "Yes",
     "No online payment gateway; single currency per store"),
]

CH2_THEORY_INTRO = (
    "The project depends on the following concepts and technologies."
)

CH2_THEORY_ITEMS = [
    ("Multi-tenancy", "serving many independent customer organisations from one running "
     "instance of an application and one database, with the data of each tenant isolated "
     "from the others [1]."),
    ("Shared-schema tenant isolation", "the isolation strategy adopted here, in which "
     "every tenant-owned table carries a tenant_id column and every query is filtered by "
     "the tenant established for the current request."),
    ("Row-level security", "a PostgreSQL feature that attaches a policy to a table so "
     "that a session can only read rows matching a condition, used here as a second line "
     "of defence behind the application-level filter [9]."),
    ("Relational data modelling", "the formal basis for representing the associations "
     "between products, variants, carts and orders without duplication, and for querying "
     "them consistently [4]."),
    ("REST", "an architectural style in which each request carries all the information "
     "needed to interpret it and the server keeps no client session state between "
     "requests [5], which suits a system whose interface is consumed by three different "
     "clients."),
    ("Role-based access control", "authorisation in which permissions are attached to "
     "roles and roles are granted to users within a particular tenant, so that one person "
     "may be an owner of one store and a staff member of another."),
    ("Server-side rendering", "producing complete HTML on the server so that storefront "
     "product pages are indexable by search engines, which a purely client-rendered "
     "application would not achieve [8]."),
    ("Object-relational mapping", "mapping database tables to application objects, used "
     "here to place the tenant filter in a single session and query layer rather than "
     "repeating it in every query [10]."),
]

# ============================================================ CHAPTER 3 =====
CH3_REQ_INTRO = (
    "Requirement analysis establishes what the system is expected to do, how well it must "
    "perform, and the resources needed to implement it. The following breakdown covers "
    "the functional and non-functional requirements of the proposed platform."
)

CH3_FUNCTIONAL = [
    ("1) Authentication and Access Control", [
        "Sellers, staff and platform administrators shall be able to register, log in and "
        "log out, with sessions carried by signed tokens.",
        "A store owner shall be able to invite staff members and assign them roles, and "
        "each role shall permit only the operations defined for it.",
        "Storefront customers shall authenticate separately from platform users, because "
        "a customer account belongs to a single store rather than to the platform.",
    ]),
    ("2) Store Provisioning and Domain Mapping", [
        "A registered seller shall be able to create a store, to which the system assigns "
        "a unique slug and a platform subdomain.",
        "A store owner shall be able to attach a custom domain, which the system verifies "
        "before serving the storefront from it.",
        "A platform administrator shall be able to approve, suspend and reinstate stores.",
    ]),
    ("3) Catalogue and Inventory Management", [
        "Sellers shall be able to create, update, publish and archive products, product "
        "variants, collections and product media.",
        "Each variant shall carry its own SKU and price, and the system shall record stock "
        "on hand and reserved stock for each variant.",
        "The system shall prevent an order that requests more units than are available.",
    ]),
    ("4) Storefront and Cart", [
        "The system shall resolve the tenant from the request host and render only that "
        "tenant's catalogue and theme.",
        "Registered and guest customers shall be able to add, update and remove cart "
        "lines, and the cart shall persist between visits.",
        "The storefront shall support product search and browsing by collection.",
    ]),
    ("5) Checkout and Order Processing", [
        "Customers shall be able to place an order with a delivery address and a cash on "
        "delivery payment method, and shall receive an order number.",
        "The system shall recompute the subtotal, discount, shipping charge and total on "
        "the server at checkout rather than trusting values sent by the client.",
        "Store staff shall be able to advance an order through its status sequence and "
        "record collection of payment on delivery.",
    ]),
    ("6) Discounts, Shipping and Reporting", [
        "Sellers shall be able to define discount codes with validity periods and minimum "
        "order values, and shipping zones with associated rates.",
        "The system shall generate sales and inventory reports for a store on demand, and "
        "a platform activity summary for administrators.",
    ]),
    ("7) Error Handling and Validation", [
        "Invalid input shall be rejected with a clear, non-technical message identifying "
        "the field at fault.",
        "A request for a host that does not map to an active store shall return a "
        "store-not-found page rather than an application error.",
        "If stock changes between adding an item to the cart and confirming the order, the "
        "customer shall be returned to the cart with the affected lines identified.",
    ]),
]

CH3_NONFUNCTIONAL = [
    ("1) Tenant Isolation", [
        "No request authenticated for one tenant shall be able to read or modify data "
        "belonging to another tenant.",
        "Isolation shall be enforced in a single data-access layer and reinforced by "
        "row-level security policies in the database.",
    ]),
    ("2) Security", [
        "Credentials shall be stored only as salted hashes using Argon2, and all traffic "
        "shall be served over HTTPS.",
        "The application shall address the OWASP Top 10 categories, in particular broken "
        "access control and identification failures [11].",
        "No card or bank data is collected or stored, because no payment gateway is "
        "integrated.",
    ]),
    ("3) Performance", [
        "A storefront catalogue page shall be returned within 3 seconds under the "
        "documented test conditions.",
        "Storefront responses shall be cached so that repeated catalogue reads do not "
        "reach the database on every request.",
    ]),
    ("4) Usability", [
        "A seller shall be able to create a store and publish a first product without "
        "training or developer assistance.",
        "The storefront shall be responsive and usable on a mobile browser.",
    ]),
    ("5) Scalability", [
        "Adding a further seller shall require no additional deployment, database or "
        "hosting account.",
        "The application tier shall be stateless so that further instances can be added "
        "behind a load balancer.",
    ]),
    ("6) Maintainability", [
        "Code shall be modular, documented and version-controlled in a Git repository.",
        "Database changes shall be applied through versioned migrations committed "
        "alongside the code that requires them.",
    ]),
]

CH3_FEAS_INTRO = (
    "The feasibility study evaluates whether the proposed platform can be developed and "
    "deployed within the available technical, operational, economic and time constraints."
)

CH3_TECHNICAL = [
    "The system is technically feasible because every required technology is mature, "
    "openly licensed and comprehensively documented.",
    "Python and FastAPI will be used for the application tier, providing request "
    "validation and generated interface documentation from declared models [7].",
    "TypeScript and Next.js will be used for the presentation tier, whose middleware can "
    "rewrite a request based on the Host header, which is exactly the mechanism required "
    "to serve many storefronts from one deployment [8].",
    "PostgreSQL will be used for storage, providing row-level security policies and JSONB "
    "columns for variant options and theme settings [9].",
    "SQLAlchemy and Alembic will provide object-relational mapping and versioned "
    "migrations [10].",
    "A standard laptop with 8 GB of RAM is sufficient for development, since the workload "
    "is dominated by database access rather than computation, and no specialised hardware "
    "is required.",
    "The team already has working knowledge of Python, JavaScript and relational "
    "databases, and the multi-tenant pattern adopted is well described in the literature "
    "[1], [2], [3].",
]

CH3_OPERATIONAL = [
    "The system is operationally feasible because the intended users already sell online, "
    "so the concepts of a catalogue, an order and a delivery address are familiar to them.",
    "The seller dashboard replaces a manual notebook rather than an existing software "
    "system, which removes the migration effort that normally blocks adoption.",
    "Store provisioning is self-service, so a seller can open a store from a registration "
    "form without contacting the platform operator.",
    "Storefronts are served over ordinary web browsers on both desktop and mobile, so "
    "customers need install nothing.",
    "Cash on delivery is retained as the settlement method because it is the method these "
    "sellers and their customers already use.",
]

CH3_ECONOMIC = [
    "The project is economically feasible because every tool in the stack is free and "
    "open source, and no commercial licence is required at any stage.",
    "Development and demonstration hosting are covered by free tiers for the application "
    "and a small managed PostgreSQL instance.",
    "The only unavoidable cost is a domain name for the demonstration deployment, which is "
    "a small annual fee.",
    "For the platform operator, the shared-database design means the marginal cost of an "
    "additional seller is the cost of the rows that seller creates, rather than the cost "
    "of a further deployment.",
]

CH3_SCHEDULE = [
    "The project is scheduled over six months, as set out in the Gantt chart in Section "
    "6.1.",
    "Requirement analysis, design, development, integration, testing, deployment and "
    "documentation are treated as separate activities, and testing is allocated its own "
    "period rather than being absorbed into development.",
    "The highest-risk element of the design, tenant isolation, is built in the first "
    "development iteration so that it is exercised by every later increment rather than "
    "being validated only at the end.",
    "Documentation runs in parallel across the whole period so that the final report does "
    "not depend on a single concentrated effort at the end.",
]

# ============================================================ CHAPTER 4 =====
CH4_OVERVIEW = [
    "Kinyo is organised as a three-tier web application consisting of a presentation tier, "
    "an application tier and a data tier. The tiers communicate only through defined "
    "interfaces, so that each can be developed, tested and deployed independently.",

    "A single deployment serves three distinct audiences. Customers reach public "
    "storefronts at a platform subdomain or at a verified custom domain. Sellers and their "
    "staff reach a dashboard at the application subdomain. Platform administrators reach "
    "an administration console. All three are served by the same presentation tier and "
    "consume the same REST interface, and the tenant that a request belongs to is "
    "established once, at the entry point, before any other processing occurs.",

    "The unit of tenancy is the store. A store owns its domains, theme, products, "
    "collections, customers, carts, orders, discounts and shipping zones. Every one of "
    "those tables carries a tenant identifier, and the platform users who administer a "
    "store are linked to it through a membership record that also carries the role held.",
]

CH4_SDLC = [
    "The iterative and incremental model has been selected for this project. In this model "
    "the system is built in a series of iterations, each passing through requirement "
    "analysis, design, implementation, testing and evaluation, and each delivering a "
    "working increment [6].",

    "The model suits this project for three reasons. First, the requirements of the seller "
    "dashboard are expected to be refined through repeated feedback from prospective "
    "sellers, and an iterative model absorbs that feedback without restarting the design. "
    "Second, the system decomposes naturally into increments that can be built and tested "
    "independently: the tenancy and authentication core, the catalogue and storefront, and "
    "finally the cart, order and administration modules. Third, tenant isolation is the "
    "highest-risk element of the design, and building it in the first iteration means it "
    "is exercised by every subsequent increment.",

    "A purely sequential waterfall model was rejected because it would defer all testing "
    "of tenant isolation until after the whole system was written. A fully agile process "
    "was rejected because the project has no permanently available product owner. The "
    "model as it will be applied is shown in Figure 1.",
]

TABLE2_ROWS = [
    ("Processor", "Intel Core i5, 8th generation or equivalent",
     "Running the development environment and local services"),
    ("RAM", "8 GB minimum, 16 GB recommended",
     "Running the database, application server and front-end build concurrently"),
    ("Storage", "40 GB free on a solid state drive",
     "Source code, dependencies, container images and the local database"),
    ("Display", "1920 x 1080 or higher",
     "Dashboard and storefront layout work"),
    ("Network", "Broadband internet connection",
     "Package installation, deployment and domain verification"),
    ("Server (deployment)", "1 vCPU, 1 GB RAM application instance and a managed "
     "PostgreSQL instance", "Hosting the demonstration deployment"),
]

TABLE3_ROWS = [
    ("Operating system", "Windows 10 or 11, or Ubuntu 22.04 LTS", "Development platform"),
    ("Back-end language", "Python 3.11", "Application tier implementation"),
    ("Back-end framework", "FastAPI with Pydantic and Uvicorn",
     "REST interface, request validation, generated API documentation"),
    ("Front-end language", "TypeScript", "Presentation tier implementation"),
    ("Front-end framework", "Next.js 15 with React and Tailwind CSS",
     "Server-rendered storefronts, seller dashboard, admin console"),
    ("Database", "PostgreSQL 16", "Relational storage with row-level security"),
    ("ORM and migrations", "SQLAlchemy 2.0 and Alembic",
     "Tenant-scoped data access and versioned schema changes"),
    ("Cache", "Redis 7", "Session data and cached storefront responses"),
    ("Object storage", "S3-compatible storage", "Product images and theme assets"),
    ("Authentication", "JSON Web Tokens with Argon2 hashing", "Session and credential handling"),
    ("Testing", "pytest and Playwright", "Unit, integration and end-to-end testing"),
    ("Containerisation", "Docker and Docker Compose", "Reproducible local environment"),
    ("IDE", "Visual Studio Code", "Development environment"),
    ("Version control", "Git and GitHub", "Source code management and collaboration"),
    ("Deployment", "Vercel for the front end, Render for the API and database",
     "Public demonstration deployment"),
]

CH4_TENANCY = [
    "The isolation strategy selected is a shared database with a shared schema, in which "
    "every tenant-owned table carries a tenant_id column referencing the store that owns "
    "the row [1]. This was chosen over a database per tenant and a schema per tenant "
    "because the target tenants are numerous and individually small, and the shared schema "
    "is the only form in which the marginal cost of an additional seller is the cost of "
    "the rows that seller creates [3].",

    "The weakness of the shared schema is that isolation depends on the application "
    "filtering every query correctly, and a single mistake exposes one tenant's data to "
    "another [2]. Three measures address this. First, the tenant established for a request "
    "is stored in a request-scoped context, and all tenant-owned models are queried "
    "through one data-access layer that applies the filter automatically, so that "
    "isolation does not depend on each query being written correctly. Second, row-level "
    "security policies in PostgreSQL restrict the rows a database session can read, so "
    "that a query which escapes the application filter still cannot reach another tenant's "
    "rows [9]. Third, a dedicated group of integration tests creates two tenants and "
    "asserts that every read and write performed under one tenant's credentials fails or "
    "returns empty for the other tenant's data.",

    "Platform users are held outside the tenant boundary, in a users table, and are "
    "connected to stores through membership records that carry the role held in that "
    "store. This allows one person to own one store and work as staff in another. "
    "Storefront customers, by contrast, are tenant-owned: a customer account created on "
    "one seller's storefront exists only for that seller.",
]

CH4_ALGO_INTRO = (
    "Three parts of the system depend on logic that is not a simple create, read, update "
    "or delete operation. Each is set out below as numbered steps."
)

ALGO_1 = ("4.5.1 Tenant Resolution Algorithm",
          "This algorithm establishes which store a request belongs to. It runs before any "
          "other processing, in the presentation tier for page requests and in the "
          "application tier for interface requests.", [
    "Read the Host header of the incoming request, convert it to lower case and remove any "
    "port suffix.",
    "If the host equals the platform application domain, mark the request as a dashboard "
    "request, resolve the tenant from the authenticated user's active membership and stop.",
    "If the host equals the platform root domain, mark the request as a marketing request "
    "with no tenant and stop.",
    "If the host ends with the platform storefront suffix, extract the leading label as the "
    "store slug and look up the store with that slug.",
    "Otherwise treat the host as a custom domain and look up a verified domain record with "
    "that host name.",
    "If no store is found, or the store status is not active, return a store-not-found "
    "response and stop.",
    "Store the identifier of the resolved tenant in the request-scoped context, load the "
    "theme settings for that tenant and continue processing the request.",
])

ALGO_2 = ("4.5.2 Cart Pricing and Discount Algorithm",
          "This algorithm computes the amount payable for a cart. It is executed whenever "
          "the cart changes and again at checkout, so that a price shown to the customer "
          "is recomputed on the server rather than trusted from the client.", [
    "Set the subtotal to zero.",
    "For each cart line, read the current price of the referenced variant, multiply it by "
    "the line quantity, store the result as the line total and add it to the subtotal.",
    "If a discount code has been supplied, retrieve the discount belonging to the current "
    "tenant with that code; if it does not exist, has expired, or its minimum order value "
    "exceeds the subtotal, reject the code and set the discount amount to zero.",
    "If the discount is valid and of percentage type, set the discount amount to the "
    "subtotal multiplied by the percentage value, rounded to two decimal places; if it is "
    "of fixed type, set the discount amount to the lesser of the fixed value and the "
    "subtotal.",
    "Determine the shipping zone containing the delivery address and read the rate defined "
    "for that zone; if no zone matches, apply the default rate of the store.",
    "Compute the total as the subtotal, minus the discount amount, plus the shipping rate.",
    "Return the subtotal, discount amount, shipping rate and total, together with the "
    "reason for any rejected discount code.",
])

ALGO_3 = ("4.5.3 Order Placement and Stock Reservation Algorithm",
          "This algorithm converts a cart into an order. It must not allow two customers to "
          "be sold the last unit of the same variant, so the stock check and the "
          "reservation are performed inside one database transaction.", [
    "Begin a database transaction.",
    "Re-read every cart line and lock the inventory row of each referenced variant for "
    "update.",
    "For each line whose variant is tracked, compare the requested quantity with the stock "
    "on hand minus the stock already reserved.",
    "If any line fails the comparison, roll back the transaction and return the cart to the "
    "customer with a stock conflict message identifying the affected lines.",
    "Recompute the cart totals using the algorithm in Section 4.5.2, so that the stored "
    "order reflects prices verified at the moment of placement.",
    "Create the order record with a generated order number, the resolved tenant, the "
    "customer, the delivery address, the computed totals, a status of pending and a "
    "payment method of cash on delivery.",
    "Create one order line for each cart line, copying the unit price into the line so that "
    "later price changes do not alter the order.",
    "Increase the reserved quantity of each tracked variant by the ordered quantity.",
    "Mark the cart as converted, commit the transaction and queue notifications to the "
    "seller and the customer.",
])

CH4_ARCH_OVERALL = [
    "The overall architecture is shown in Figure 2. A request from any of the three client "
    "types first reaches the tenant resolution middleware in the Next.js application, "
    "which reads the Host header and applies the algorithm of Section 4.5.1. The request "
    "is then rewritten to the storefront routes, the seller dashboard or the platform "
    "console according to the host that was matched.",

    "Storefront pages are rendered on the server, so that a product page is delivered to "
    "the browser as complete HTML and can be indexed by search engines. The rendering "
    "process requests the data it needs from the application tier over HTTPS, using the "
    "same REST interface that the dashboard and the console use.",

    "The application tier authorises the request, applies the tenant filter in the "
    "data-access layer and queries PostgreSQL. Product media is served from object "
    "storage rather than through the application, and Redis holds cached storefront "
    "responses and session data so that repeated catalogue reads do not reach the "
    "database on every request.",
]

CH4_COMPONENTS = [
    ("Tenant resolution middleware", "reads the Host header on every request, resolves it "
     "to a store, and rewrites the request to the storefront, dashboard or console routes. "
     "Returns a store-not-found response when no active store matches."),
    ("Storefront pages", "server-rendered catalogue, product, collection, cart and "
     "checkout pages, styled by the theme settings of the resolved tenant."),
    ("Seller dashboard", "the interface through which a store owner and staff manage the "
     "catalogue, inventory, discounts, shipping, staff, orders and reports."),
    ("Platform admin console", "the interface through which platform administrators "
     "approve, suspend and monitor stores."),
    ("Authentication and RBAC service", "registers and authenticates platform users, "
     "issues and validates signed tokens, and evaluates role permissions within a tenant."),
    ("Tenant and domain service", "creates stores, allocates slugs and subdomains, records "
     "custom domains and performs domain verification."),
    ("Catalogue and inventory service", "maintains products, variants, collections, media "
     "and stock levels, including reservation and release of stock."),
    ("Cart and order service", "maintains carts, computes pricing, converts carts into "
     "orders inside a transaction and advances orders through their status sequence."),
    ("Reporting service", "aggregates order and catalogue data into sales and inventory "
     "reports for sellers and an activity summary for administrators."),
    ("Data-access layer", "the single point at which the tenant filter is applied to every "
     "query against a tenant-owned model, built on the SQLAlchemy ORM."),
    ("PostgreSQL database", "the shared relational store, with tenant_id on every "
     "tenant-owned table and row-level security policies as a second line of defence."),
    ("Redis", "cached storefront responses and session data."),
    ("Object storage", "product images and theme assets, served directly to browsers."),
]

CH4_WORKFLOW = [
    "Figure 3 shows the sequence of operations performed by the system from the moment a "
    "visitor opens a storefront address to the moment an order is confirmed. The chart is "
    "divided into three stages connected by numbered off-page connectors.",

    "Stage A resolves the store and serves the catalogue. The middleware extracts the Host "
    "header and applies the tenant resolution algorithm; if no active store matches, the "
    "visitor is shown a store-not-found page and the flow ends. Otherwise the tenant "
    "context and theme are loaded and the catalogue for that tenant is rendered. When the "
    "customer adds an item, the system checks that the chosen variant is in stock before "
    "creating or updating the cart line.",

    "Stage B collects the information needed to complete the order and computes the amount "
    "payable. A customer who is not authenticated supplies contact details as a guest. The "
    "delivery address is collected and the totals are computed by the algorithm of Section "
    "4.5.2; an invalid discount code is rejected and the totals are recomputed before the "
    "order summary is confirmed.",

    "Stage C creates the order. The stock check is repeated at this point, because stock "
    "may have changed while the customer was completing the checkout. If it fails, the "
    "customer is returned to the cart. If it succeeds, the order is created and inventory "
    "is reserved in one transaction, the payment method is recorded as cash on delivery, "
    "the seller and customer are notified, and the confirmation is displayed.",
]

CH4_CONTEXT = [
    "The context diagram in Figure 4 represents the whole platform as a single process and "
    "shows the data that crosses its boundary. Four external entities interact with the "
    "system. The store owner supplies store details, product data, and discount and "
    "shipping rules, and receives the store dashboard, sales reports and order alerts. "
    "Store staff supply stock updates and fulfilment status, and receive the order queue "
    "and inventory alerts. The customer supplies search terms, cart items and order and "
    "address details, and receives product listings, cart summaries and order status. The "
    "platform administrator supplies store approval decisions and platform settings, and "
    "receives the store registry and a platform activity summary.",
]

CH4_DFD1 = [
    "Figure 5 decomposes the single process of Figure 4 into six processes and six data "
    "stores. Process 1.0, Manage Users and Access, authenticates platform users and issues "
    "session tokens against the user and role store. Process 2.0, Provision Store and "
    "Domain, creates tenant records and domain mappings and applies the administrator's "
    "approval decisions. Process 3.0, Manage Catalog and Inventory, maintains products, "
    "variants and stock levels. Process 4.0, Serve Storefront and Cart, resolves the "
    "tenant, reads the catalogue and maintains cart records. Process 5.0, Process Order, "
    "converts a cart into an order, reserves stock, records the customer and reports "
    "fulfilment progress. Process 6.0, Generate Reports, reads order and catalogue data to "
    "produce sales reports for sellers and an activity summary for administrators.",

    "The data stores correspond to the entity groups of Section 4.7.4: D1 holds users and "
    "roles, D2 tenants and domains, D3 products and inventory, D4 carts, D5 orders and D6 "
    "storefront customers. Every store except D1 is partitioned internally by tenant "
    "identifier.",
]

CH4_USECASE = [
    "The use case diagram in Figure 6 shows the interactions between the actors and the "
    "system. Five actors are involved. The platform administrator approves and suspends "
    "stores and monitors platform-wide activity. The store owner creates and configures a "
    "store, maps its subdomain and custom domain, customises the storefront theme, defines "
    "discounts and shipping zones, manages staff and roles, and views sales reports. Store "
    "staff manage the product catalogue and its variants, maintain inventory levels, and "
    "process and fulfil orders. The registered customer creates a customer account, "
    "browses and searches the storefront, manages a cart, places orders and tracks their "
    "status. The guest visitor may browse, manage a cart and place an order without "
    "creating an account.",

    "The system supports 17 primary use cases across these five actor roles. Registration "
    "and authentication is shared between the platform administrator and the store owner "
    "because both are platform users, while storefront customers authenticate separately "
    "through the customer account use case.",
]

CH4_ERD = [
    "The entity relationship diagram in Figure 7 shows the principal entities of the "
    "database, their primary and foreign keys and the cardinality of each relationship. "
    "TENANT is the root of the tenant-owned data: a tenant has many domains, products, "
    "collections, customers, carts, orders, discounts and shipping zones, and each of "
    "those tables carries tenant_id as a foreign key referencing TENANT. Platform users "
    "are held separately in USER and connected to tenants through MEMBERSHIP, which "
    "carries the role held by that user in that tenant.",

    "In the catalogue, a PRODUCT has many PRODUCT_VARIANT rows, each identified by a "
    "unique SKU and carrying its own price, and each variant has exactly one "
    "INVENTORY_ITEM recording stock on hand and stock reserved. Products are grouped into "
    "collections through a many-to-many association. In the commerce path, a CUSTOMER "
    "saves many addresses and owns carts and orders; a CART contains many CART_ITEM rows "
    "and an ORDERS row contains many ORDER_ITEM rows, each referring to a variant and "
    "storing the unit price agreed at the time of purchase. An order also references the "
    "address it ships to, the discount applied and the shipping zone that priced it.",

    "Supporting tables not drawn in Figure 7, in order to keep the diagram legible, are "
    "the theme settings of a store, product media assets, shipment tracking records and "
    "platform-level role definitions. Each follows the same rule as the entities shown: it "
    "carries tenant_id where it is tenant-owned, and its primary key is a universally "
    "unique identifier.",
]

# ============================================================ CHAPTER 5 =====
CH5_INTRO = (
    "This chapter describes the anticipated results of the project. Everything stated here "
    "is an expectation to be verified during testing, not a result already obtained."
)

CH5_OUTCOMES = [
    "A deployed multi-tenant web application in which a seller can register, create a "
    "store, publish a catalogue and receive orders, and in which a customer can browse a "
    "storefront and place an order settled by cash on delivery.",
    "A seller dashboard covering catalogue, inventory, discount, shipping, staff and order "
    "management, and a platform administration console for approving and suspending "
    "stores.",
    "Server-rendered storefronts reachable at platform subdomains and at verified custom "
    "domains, each rendering only the catalogue and theme of its own tenant.",
    "The complete source code of the back-end and front-end applications, with setup "
    "instructions and interface documentation generated from the code.",
    "The database schema as a versioned sequence of migrations, together with a seed "
    "dataset of sample stores, products and orders for demonstration.",
    "A documented test suite and a completed test case table recording the outcome of each "
    "defined test case, including the cross-tenant isolation cases.",
    "A public Git repository containing all code, migrations and documentation.",
]

CH5_EVAL_INTRO = (
    "Because the proposed system is a web platform rather than a predictive model, it is "
    "evaluated against functional, isolation, performance and usability criteria rather "
    "than statistical accuracy metrics. The criteria below define what will be measured "
    "and how."
)

CH5_EVAL_SECTIONS = [
    ("5.2.1 Functional Test Coverage", [
        "Forty test cases are defined across authentication and access control, tenant "
        "isolation, catalogue and inventory, cart and pricing, order placement, and "
        "storefront routing.",
        "Each case is recorded in a table with the columns test case identifier, module, "
        "precondition, input, expected output, actual result and status.",
        "Unit tests cover each service module in isolation using a transactional test "
        "database, with table-driven cases including boundary values such as a zero-stock "
        "variant and an expired discount code.",
        "Integration tests exercise the interface end to end, covering registration, store "
        "provisioning, catalogue creation, cart operations and order placement.",
    ]),
    ("5.2.2 Tenant Isolation Verification", [
        "A dedicated group of tests creates two tenants with overlapping data, such as "
        "products with identical SKUs and customers with identical email addresses.",
        "Every read and write operation available in the interface is then attempted under "
        "one tenant's credentials against the other tenant's identifiers.",
        "The expected result in every case is a not-found or forbidden response, never a "
        "successful read or a partial disclosure.",
        "The same suite is run a second time with the application-level filter disabled, to "
        "confirm that the PostgreSQL row-level security policies independently block the "
        "access.",
    ]),
    ("5.2.3 System Performance Criteria", [
        "Storefront catalogue page response time, measured under the documented test "
        "conditions, with a target below 3 seconds.",
        "Application programming interface response time for catalogue and cart "
        "operations, with a target below 1 second.",
        "Order placement transaction time, including the stock reservation, with a target "
        "below 2 seconds.",
        "Availability of the demonstration deployment during the acceptance testing "
        "period, with a target above 95 per cent.",
    ]),
    ("5.2.4 Usability and Acceptance Criteria", [
        "A prospective seller who has not used the system before completes store creation "
        "and publication of a first product without assistance.",
        "A prospective customer completes a purchase from browsing to order confirmation "
        "without assistance.",
        "Store staff advance an order through its full status sequence and record "
        "collection of payment on delivery.",
        "Task completion and the difficulties encountered are recorded for each "
        "participant during user acceptance testing.",
    ]),
]

TABLE4_ROWS = [
    ("Functional test cases passed", "40 of 40", "Test case table"),
    ("Cross-tenant access attempts blocked", "100 per cent",
     "Isolation test suite, run with and without the application filter"),
    ("Storefront page response time", "Below 3 seconds",
     "Timed requests under documented test conditions"),
    ("API response time (catalogue and cart)", "Below 1 second", "Timed requests"),
    ("Order placement transaction time", "Below 2 seconds", "Timed requests"),
    ("Deployment availability", "Above 95 per cent",
     "Uptime monitoring during acceptance testing"),
    ("Seller task completion without assistance", "All participants",
     "User acceptance testing"),
    ("Customer purchase completion without assistance", "All participants",
     "User acceptance testing"),
]

CH5_ACCEPTANCE_INTRO = (
    "The system will be considered successful if all of the following hold:"
)

CH5_ACCEPTANCE = [
    "All 40 defined functional test cases pass.",
    "No cross-tenant read or write succeeds in the isolation test suite, either with or "
    "without the application-level filter enabled.",
    "Storefront pages respond within 3 seconds and interface calls within 1 second under "
    "the documented test conditions.",
    "Every participant in user acceptance testing completes the assigned seller and "
    "customer tasks without assistance.",
    "The demonstration deployment serves storefronts correctly at both a platform "
    "subdomain and a verified custom domain.",
]

CH5_ACCEPTANCE_TAIL = (
    "If any criterion is not met, the affected module will be revised and the relevant "
    "tests re-run before the system is presented as complete."
)

# ============================================================ CHAPTER 6 =====
CH6_GANTT = [
    "A Gantt chart is a project management tool used to plan, schedule and track tasks "
    "over time. It represents project activities along a timeline, showing the duration of "
    "each task and the overlap between tasks, so that progress can be monitored and delays "
    "identified. The Gantt chart for the proposed system is shown in Figure 8.",

    "The schedule allocates the first two months to requirement analysis, literature "
    "review and system design, so that the data model and the tenancy strategy are settled "
    "before any application code is written. Development is split into three increments "
    "that follow the iterative model described in Section 4.2: the tenancy and "
    "authentication core, the catalogue and storefront, and finally the cart, order and "
    "administration modules. Testing is given its own period in months five and six rather "
    "than being absorbed into development, and documentation runs across the whole "
    "project period.",
]

# ============================================================ REFERENCES ====
REFERENCES = [
    "F. Chong and G. Carraro, “Architecture strategies for catching the long tail,” "
    "Microsoft Corporation, 2006. [Online]. Available: "
    "https://learn.microsoft.com/en-us/previous-versions/dotnet/articles/aa479069(v=msdn.10)",

    "C.-P. Bezemer and A. Zaidman, “Multi-tenant SaaS applications: Maintenance dream "
    "or nightmare?” in Proc. Joint ERCIM Workshop on Software Evolution and Int. "
    "Workshop on Principles of Software Evolution, Antwerp, Belgium, 2010, pp. 88–92.",

    "R. Krebs, C. Momm, and S. Kounev, “Architectural concerns in multi-tenant SaaS "
    "applications,” in Proc. 2nd Int. Conf. on Cloud Computing and Services Science, "
    "Porto, Portugal, 2012, pp. 426–431.",

    "E. F. Codd, “A relational model of data for large shared data banks,” "
    "Communications of the ACM, vol. 13, no. 6, pp. 377–387, 1970.",

    "R. T. Fielding, “Architectural styles and the design of network-based software "
    "architectures,” Ph.D. dissertation, Univ. of California, Irvine, CA, USA, 2000.",

    "I. Sommerville, Software Engineering, 10th ed. Harlow, U.K.: Pearson, 2016.",

    "“FastAPI documentation,” 2024. [Online]. Available: "
    "https://fastapi.tiangolo.com/",

    "“Next.js documentation,” Vercel, 2024. [Online]. Available: "
    "https://nextjs.org/docs",

    "“PostgreSQL 16 documentation,” PostgreSQL Global Development Group, 2024. "
    "[Online]. Available: https://www.postgresql.org/docs/16/",

    "“SQLAlchemy 2.0 documentation,” 2024. [Online]. Available: "
    "https://docs.sqlalchemy.org/en/20/",

    "“OWASP Top 10:2021,” Open Web Application Security Project, 2021. [Online]. "
    "Available: https://owasp.org/Top10/",

    "“Shopify developer documentation,” Shopify, 2024. [Online]. Available: "
    "https://shopify.dev/docs",

    "“WooCommerce documentation,” WooCommerce, 2024. [Online]. Available: "
    "https://woocommerce.com/documentation/",

    "“Saleor documentation,” Saleor Commerce, 2024. [Online]. Available: "
    "https://docs.saleor.io/",

    "“Medusa documentation,” Medusa, 2024. [Online]. Available: "
    "https://docs.medusajs.com/",

    "“Nepal country commercial guide: eCommerce,” International Trade "
    "Administration, U.S. Department of Commerce, 2024. [Online]. Available: "
    "https://www.trade.gov/country-commercial-guides/nepal-ecommerce",
]
