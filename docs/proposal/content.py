"""All prose, tables and metadata for the Kinyo Project-VI proposal.

Placeholders in square brackets must be replaced before submission.
Kept separate from build_docx.py so the wording can be edited without touching
the APA formatting code.
"""

# ---------------------------------------------------------------- metadata --
META = {
    "university": "PURBANCHAL UNIVERSITY",
    "college": "HIMALAYAN WHITEHOUSE INTERNATIONAL COLLEGE",
    "college_address": "Putalisadak, Kathmandu",
    "title": "Kinyo: A Multi-Tenant E-Commerce Platform for Independent Sellers",
    "semester_line": "8th Semester Apprenticeship Project",
    "students": [
        ("Hikmat Baniya", "15"),
        ("Nishan Neupane", "23"),
    ],
    "supervisor": "[Supervisor Name]",
    "city": "Kathmandu",
    "month_year": "September, 2026",
    "repo_backend": "https://github.com/HikmatBaniya/kinyo",
    "repo_frontend": "https://github.com/HikmatBaniya/kinyo-front",
}

MONTHS = ["M1", "M2", "M3", "M4", "M5", "M6"]

# ----------------------------------------------------------------- abstract --
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

# ------------------------------------------------------------ abbreviations --
ABBREVIATIONS = [
    ("API", "Application Programming Interface"),
    ("CDN", "Content Delivery Network"),
    ("CNAME", "Canonical Name (Domain Name System record)"),
    ("COD", "Cash on Delivery"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("CSS", "Cascading Style Sheets"),
    ("CSV", "Comma-Separated Values"),
    ("DFD", "Data Flow Diagram"),
    ("DNS", "Domain Name System"),
    ("ER", "Entity Relationship"),
    ("HTML", "HyperText Markup Language"),
    ("HTTP", "HyperText Transfer Protocol"),
    ("HTTPS", "HyperText Transfer Protocol Secure"),
    ("IDE", "Integrated Development Environment"),
    ("JSON", "JavaScript Object Notation"),
    ("JWT", "JSON Web Token"),
    ("MVC", "Model-View-Controller"),
    ("ORM", "Object-Relational Mapping"),
    ("OWASP", "Open Web Application Security Project"),
    ("PK", "Primary Key"),
    ("FK", "Foreign Key"),
    ("RAM", "Random Access Memory"),
    ("RBAC", "Role-Based Access Control"),
    ("REST", "Representational State Transfer"),
    ("RLS", "Row-Level Security"),
    ("SaaS", "Software as a Service"),
    ("SDLC", "Software Development Life Cycle"),
    ("SEO", "Search Engine Optimisation"),
    ("SKU", "Stock Keeping Unit"),
    ("SME", "Small and Medium Enterprise"),
    ("SQL", "Structured Query Language"),
    ("SSR", "Server-Side Rendering"),
    ("UAT", "User Acceptance Testing"),
    ("UI", "User Interface"),
    ("UML", "Unified Modeling Language"),
    ("URL", "Uniform Resource Locator"),
    ("UUID", "Universally Unique Identifier"),
    ("UX", "User Experience"),
]

# ------------------------------------------------------------------ figures --
FIGURES = {
    1: ("SDLC Model: Iterative and Incremental Development", "fig1_sdlc.png", 6.1),
    2: ("Gantt Chart", None, None),          # supplied separately
    3: ("System Architecture of the Kinyo Platform", "fig2_architecture.png", 6.1),
    4: ("System Flowchart: Storefront Resolution to Order Confirmation",
        "fig3_flowchart.png", 5.9),
    5: ("Use Case Diagram", "fig4_usecase.png", 6.0),
    6: ("Data Flow Diagram: Level 0 (Context Diagram)", "fig5_dfd0.png", 6.1),
    7: ("Data Flow Diagram: Level 1", "fig6_dfd1.png", 6.1),
    8: ("Entity Relationship (ER) Diagram", "fig7_erd.png", 5.8),
}

TABLE_TITLES = {}

# =========================================================== CHAPTER 1 =======
CH1_BACKGROUND = [
    "Retail trade in Nepal is dominated by small and medium enterprises that operate "
    "from a single shop and sell to a local customer base. Over the past decade a large "
    "share of these sellers has moved part of that trade online, but the move has been "
    "made almost entirely through general-purpose social media pages and messaging "
    "applications rather than through owned sales channels. A seller typically publishes "
    "product photographs on a social media page, negotiates price and availability in "
    "private messages, records the resulting orders in a notebook or a spreadsheet, and "
    "arranges delivery by telephone. The country commercial guidance published for Nepal "
    "notes that online retail is expanding quickly while the supporting commercial "
    "infrastructure remains uneven (International Trade Administration, 2024).",

    "This way of working has clear shortcomings. The seller does not control the "
    "presentation of the catalogue, cannot show reliable stock levels, and has no record "
    "of an order beyond a chat history that is easily lost. Prices, discounts and delivery "
    "charges are re-negotiated for every customer. Because the storefront is a page inside "
    "someone else's platform, the seller cannot be found through ordinary web search, "
    "cannot build a branded identity, and cannot export a customer list.",

    "The established alternative is a hosted commerce platform. Systems such as Shopify "
    "and Wix eCommerce allow a seller to create a branded online store without writing "
    "code, and open-source systems such as WooCommerce, Saleor and Medusa allow the same "
    "outcome for a seller who can pay for development and hosting (Shopify, 2024; "
    "Saleor Commerce, 2024). These systems are mature, but each of them assumes either a "
    "recurring subscription paid in foreign currency or a level of technical skill that an "
    "average Nepali shop owner does not have.",

    "The project proposed here, named Kinyo, is a multi-tenant e-commerce platform on "
    "which many independent sellers operate their own branded storefronts from a single "
    "deployed application. Multi-tenancy is the architectural practice of serving many "
    "customer organisations, called tenants, from one running instance of an application "
    "and one database, with the data of each tenant isolated from the others "
    "(Chong & Carraro, 2006). Applying that practice here allows the cost of hosting, "
    "maintenance and upgrades to be shared across all sellers, which is what makes an "
    "affordable, locally operated storefront service possible.",
]

CH1_PROBLEM = [
    "Independent retailers in Nepal who wish to sell online have no affordable way to "
    "obtain and operate a storefront that they control. The current process depends on "
    "social media pages and manual record keeping: the catalogue is a series of image "
    "posts, the order book is a chat thread, and stock is tracked from memory. As a "
    "consequence, orders are lost or duplicated, items are sold after they are out of "
    "stock, pricing and delivery charges are inconsistent between customers, and no "
    "sales history exists from which the seller could plan purchasing.",

    "The parties that bear the cost of this gap are the sellers, who lose sales and spend "
    "unpaid hours on manual coordination, and their customers, who cannot see accurate "
    "availability, cannot check the status of an order, and have no record of what they "
    "agreed to buy. Existing marketplace applications do not close the gap, because a "
    "seller listed inside a marketplace does not own the storefront, the customer "
    "relationship or the presentation of the brand. Existing hosted platforms do not close "
    "it either, because their subscription pricing and configuration effort place them "
    "beyond the reach of a single-shop retailer.",

    "There is currently no system that provides a Nepali independent seller with a "
    "self-service branded storefront, an accurate catalogue with variant-level stock "
    "control, and a recorded order lifecycle, at a cost that a single-shop business can "
    "sustain. The absence of such a system keeps small retailers dependent on manual, "
    "error-prone processes and prevents them from competing online with larger sellers.",
]

CH1_GENERAL_OBJECTIVE = (
    "To design, develop and deploy Kinyo, a multi-tenant e-commerce platform that enables "
    "independent sellers to create, customise and operate their own branded online "
    "storefronts from a single shared application."
)

CH1_SPECIFIC_OBJECTIVES = [
    "To analyse the requirements of independent sellers and their customers for online "
    "catalogue management, storefront presentation and order handling.",
    "To design a shared-database multi-tenant data model and a three-tier system "
    "architecture in which every tenant-owned record is isolated by a tenant identifier.",
    "To implement the store provisioning, catalogue, cart and order modules, including "
    "host-based storefront routing, and to verify them against 40 defined test cases "
    "covering functional behaviour and cross-tenant data isolation.",
    "To deploy the platform as a web application that serves seller dashboards and "
    "customer storefronts over subdomain and custom-domain addresses.",
]

CH1_SCOPE_INTRO = (
    "The boundaries of the project are defined below. The system is a storefront and "
    "order-management platform; it is not an accounting system, a marketplace or a "
    "logistics system."
)

CH1_SCOPE_ITEMS = [
    ("Features included",
     "seller registration and role-based staff access; store provisioning; subdomain and "
     "custom-domain mapping; storefront theme selection and customisation; product "
     "catalogue with variants, collections and media; variant-level inventory tracking; "
     "shopping cart for registered and guest customers; checkout and order placement; "
     "order status and fulfilment tracking; discount codes; shipping zones and rates; "
     "sales reporting for sellers; and a platform administration console for approving "
     "and suspending stores."),
    ("Target users",
     "independent retailers and their staff who sell physical goods; the customers who "
     "buy from those storefronts; and the platform administrators who operate Kinyo."),
    ("Scope of functionality",
     "the system will manage storefronts, catalogues, inventory, carts and the order "
     "lifecycle. It will not perform accounting, tax filing or bookkeeping, will not "
     "integrate an online payment gateway, and will not manage warehousing or courier "
     "dispatch. Orders are completed using cash on delivery, and the payment status is "
     "recorded manually by the seller. Online payment integration is identified as future "
     "work and is deliberately excluded so that the multi-tenant storefront functionality "
     "can be completed and tested within the academic timeframe."),
    ("Deployment scope",
     "the system will be delivered as a web application, comprising a browser-based seller "
     "dashboard, a browser-based platform administration console, and server-rendered "
     "public storefronts. Native mobile applications are out of scope; the storefronts "
     "will be responsive and usable on mobile browsers."),
]

# =========================================================== CHAPTER 2 =======
CH2_THEORY = [
    "The project rests on three bodies of technical practice: multi-tenant application "
    "architecture, relational data modelling, and the design of stateless web application "
    "programming interfaces. Each is described below together with the reason it was "
    "adopted.",

    "Multi-tenancy. A multi-tenant application serves several independent customer "
    "organisations from one running instance. Chong and Carraro (2006) distinguish three "
    "approaches to isolating tenant data: a separate database for each tenant, a shared "
    "database with a separate schema for each tenant, and a shared database with a shared "
    "schema in which every tenant-owned row carries a tenant identifier. The three "
    "approaches trade isolation against cost: separate databases give the strongest "
    "isolation and the highest per-tenant operating cost, while the shared schema gives "
    "the lowest cost and requires the application to enforce isolation on every query. "
    "Krebs et al. (2012) reach the same conclusion from a performance standpoint and note "
    "that the shared-schema form is the only one that scales economically to large numbers "
    "of small tenants. Bezemer and Zaidman (2010) add the maintenance argument: a single "
    "shared instance means that a defect is fixed once for every tenant, but it also means "
    "that a defect in the isolation logic is exposed to every tenant at once. Kinyo adopts "
    "the shared-database, shared-schema model, because its target tenants are numerous and "
    "individually small, and it treats tenant isolation as a first-class correctness "
    "requirement that is tested explicitly rather than assumed.",

    "Relational data modelling. The catalogue, cart and order data of a commerce system "
    "are highly relational: a product has many variants, a variant has one stock record, "
    "an order has many line items, and each of those line items refers to a variant. The "
    "relational model gives a formal basis for representing those associations without "
    "duplication and for querying them consistently (Codd, 1970). The schema described in "
    "Section 3.8 is normalised to third normal form, with the deliberate exception that "
    "the unit price of a cart or order line is stored on the line rather than read from "
    "the variant, so that an order preserves the price that the customer actually agreed "
    "to when a product price later changes.",

    "Stateless web APIs. The application layer exposes its behaviour as a REST interface. "
    "REST is an architectural style in which each request carries all the information "
    "needed to interpret it, resources are addressed by uniform identifiers, and the "
    "server keeps no client session state between requests (Fielding, 2000). A stateless "
    "interface suits this project because the seller dashboard, the platform console and "
    "the server-rendered storefronts are three different clients of the same interface, "
    "and because authentication can then be carried in a signed token rather than in "
    "server-side session storage.",

    "Access control. Two distinct populations authenticate against the system: platform "
    "users, who are sellers, their staff and platform administrators, and storefront "
    "customers, who belong to a single tenant. Platform users are authorised through "
    "role-based access control, in which permissions are attached to roles and roles are "
    "granted to users within a particular tenant, so that the same person may be an owner "
    "of one store and a staff member of another. The security requirements for both "
    "populations follow the categories of the OWASP Top 10, in particular broken access "
    "control and identification failures (Open Web Application Security Project, 2021).",

    "Three-tier organisation. The system is organised into a presentation tier, an "
    "application tier and a data tier, described in Section 3.3. This separation was "
    "chosen over a single monolithic web application because the presentation tier must "
    "render public storefronts for search engine visibility, while the application tier "
    "must serve several different clients; keeping them apart allows each to be developed, "
    "tested and deployed independently.",
]

# Table 1 rows: author/system, platform, technique, features, limitations
TABLE1_ROWS = [
    ("Shopify (2024)", "Hosted SaaS, web",
     "Proprietary multi-tenant SaaS with a template language for themes",
     "Store provisioning, catalogue, checkout, custom domains, app ecosystem",
     "Recurring subscription priced in foreign currency; storefront logic is not "
     "modifiable; no local payment or delivery integration for Nepal"),
    ("WooCommerce (2024)", "Self-hosted, web",
     "WordPress plugin over a single-site PHP and MySQL stack",
     "Open source, large plugin catalogue, full control of the storefront",
     "Single tenant per installation; each seller must obtain hosting, install and "
     "maintain the system separately"),
    ("Adobe (2024)", "Self-hosted or cloud, web",
     "Modular PHP commerce framework with multi-store support",
     "Multiple storefronts from one installation, rich catalogue and pricing rules",
     "Very high hardware and expertise requirements; multi-store support assumes a "
     "single owning business rather than unrelated tenants"),
    ("Wix.com (2024)", "Hosted SaaS, web",
     "Proprietary multi-tenant website builder with a commerce module",
     "Drag-and-drop storefront design, hosting and domain management included",
     "Storefront structure is fixed by the builder; data export is limited; "
     "subscription priced in foreign currency"),
    ("Saleor Commerce (2024)", "Self-hosted, web",
     "Python and Django core exposing a GraphQL API with a separate storefront",
     "Modern API-first design, strong catalogue and channel model, open source",
     "Aimed at development teams; no self-service tenant onboarding; a separate "
     "deployment is expected for each merchant"),
    ("Medusa (2024)", "Self-hosted, web",
     "Node.js commerce engine with a headless API and admin application",
     "Modular services, open source, flexible order and pricing model",
     "Single-merchant by default; multi-tenancy must be added by the integrator; "
     "requires a developer to operate"),
]

CH2_TABLE1_DISCUSSION = [
    "The systems reviewed in Table 1 fall into two groups. The hosted platforms (Shopify, "
    "2024; Wix.com, 2024) already solve the multi-tenant problem: one running system "
    "serves many sellers, and a seller can open a store without technical help. Their "
    "limitation for this project's users is commercial and contextual rather than "
    "technical, namely subscription pricing in foreign currency and the absence of any "
    "adaptation to local delivery and settlement practice. The open-source platforms "
    "(WooCommerce, 2024; Adobe, 2024; Saleor Commerce, 2024; Medusa, 2024) remove the "
    "subscription cost and give full control of the code, but every one of them is built "
    "around a single merchant per deployment. Making them serve many independent sellers "
    "requires either a separate installation, database and hosting account per seller, or "
    "substantial custom development to add tenancy.",

    "The gap that this project addresses lies between those two groups: an open, "
    "self-hosted platform that is multi-tenant by design, so that one deployment can "
    "onboard many unrelated sellers through self-service, and that is shaped around the "
    "way small Nepali retailers actually sell, including cash on delivery as the default "
    "settlement method.",
]

CH2_CONTRIBUTION_INTRO = (
    "Based on the limitations identified in Section 2.2, the proposed system contributes "
    "the following."
)

CH2_CONTRIBUTION_ITEMS = [
    "Self-service multi-tenancy on an open stack. Unlike WooCommerce, Saleor and Medusa, "
    "which assume one deployment per merchant, Kinyo provisions a new tenant, its "
    "subdomain and its storefront from a registration form, with no additional "
    "installation or hosting account. A single deployment therefore serves an arbitrary "
    "number of sellers.",
    "Tenant isolation enforced and tested, not assumed. Every tenant-owned table carries a "
    "tenant identifier, queries are scoped through a single tenancy layer in the ORM, and "
    "cross-tenant access is covered explicitly by the test cases defined in Section 4.3. "
    "This responds directly to the maintenance risk that Bezemer and Zaidman (2010) "
    "identify in shared-instance systems.",
    "Host-based storefront routing with custom domains. The presentation tier resolves the "
    "tenant from the HTTP Host header, so a storefront is reachable both at a platform "
    "subdomain and at a domain owned by the seller. This gives an independent seller the "
    "branded presence that a marketplace listing cannot provide.",
    "A workflow shaped for local practice. The order lifecycle treats cash on delivery as "
    "a first-class settlement method with an explicit fulfilment and collection state, "
    "rather than as an exception to card payment, and prices are held in a single "
    "tenant-level currency.",
    "An integration that existing systems keep separate. Catalogue, variant-level "
    "inventory and the order lifecycle are managed in one application with one data model, "
    "so that stock is reserved at the moment an order is created rather than reconciled "
    "afterwards from a separate record.",
]

# Table 2 rows: type, description, priority
TABLE2_ROWS = [
    ("Functional: user authentication",
     "Users shall be able to register, log in and log out securely, and sessions shall be "
     "carried by signed tokens.", "High"),
    ("Functional: role-based access",
     "A store owner shall be able to invite staff and assign roles, and each role shall "
     "permit only the operations defined for it.", "High"),
    ("Functional: store provisioning",
     "A registered seller shall be able to create a store, which the system shall assign a "
     "unique slug and subdomain.", "High"),
    ("Functional: domain mapping",
     "A store owner shall be able to attach a custom domain, and the system shall verify "
     "it before serving the storefront from it.", "Medium"),
    ("Functional: catalogue management",
     "Sellers shall be able to create, update, publish and archive products, variants, "
     "collections and product media.", "High"),
    ("Functional: inventory management",
     "The system shall record stock on hand and reserved stock for each variant and shall "
     "prevent an order that exceeds available stock.", "High"),
    ("Functional: storefront rendering",
     "The system shall resolve the tenant from the request host and render only that "
     "tenant's catalogue and theme.", "High"),
    ("Functional: shopping cart",
     "Registered and guest customers shall be able to add, update and remove cart lines, "
     "and the cart shall persist between visits.", "High"),
    ("Functional: checkout and orders",
     "Customers shall be able to place an order with a shipping address and a cash on "
     "delivery payment method, and shall receive an order number.", "High"),
    ("Functional: order fulfilment",
     "Store staff shall be able to advance an order through its status sequence and record "
     "collection of payment.", "High"),
    ("Functional: discounts and shipping",
     "Sellers shall be able to define discount codes and shipping zones with rates that "
     "are applied during checkout.", "Medium"),
    ("Functional: reporting",
     "The system shall generate sales and inventory reports for a store on demand, and a "
     "platform activity summary for administrators.", "Medium"),
    ("Non-functional: tenant isolation",
     "No request authenticated for one tenant shall be able to read or modify data "
     "belonging to another tenant.", "High"),
    ("Non-functional: security",
     "Credentials shall be stored only as salted hashes, all traffic shall be served over "
     "HTTPS, and the application shall address the OWASP Top 10 categories.", "High"),
    ("Non-functional: performance",
     "A storefront catalogue page shall be returned within 3 seconds under the documented "
     "test conditions.", "Medium"),
    ("Non-functional: usability",
     "A seller shall be able to create a store and publish a first product without "
     "training or developer assistance.", "Medium"),
    ("Non-functional: portability",
     "The system shall run on the documented environment, and in containers, without "
     "modification to the source code.", "Medium"),
    ("Non-functional: maintainability",
     "Code shall be modular, documented and version-controlled in a Git repository, and "
     "database changes shall be applied through migrations.", "Medium"),
]

# Table 3 rows: type, analysis, verdict
TABLE3_ROWS = [
    ("Technical",
     "The team has working knowledge of Python, JavaScript and relational databases. "
     "FastAPI, Next.js, PostgreSQL and SQLAlchemy are mature, openly licensed and "
     "comprehensively documented, and all development tooling is free of charge. "
     "The multi-tenant pattern adopted is well described in the literature.", "Feasible"),
    ("Operational",
     "The intended users already sell online through social media, so the concepts of a "
     "catalogue, an order and a delivery address are familiar. The seller dashboard "
     "replaces a manual notebook rather than an existing system, which lowers the barrier "
     "to adoption. Storefronts are served over ordinary web browsers.", "Feasible"),
    ("Economic",
     "Development uses free and open-source software throughout. Hosting during "
     "development and demonstration is covered by free tiers for the application and a "
     "small managed database instance. The only unavoidable cost is a domain name for the "
     "demonstration deployment.", "Feasible"),
    ("Schedule",
     "The six-month timeline in Table 4 allocates separate periods to requirement "
     "analysis, design, development, integration, testing and documentation, with testing "
     "given its own period rather than being merged into development.", "Feasible"),
    ("Legal and ethical",
     "The system stores personal data of storefront customers, namely name, contact "
     "details and delivery address. That data is collected only for order fulfilment, is "
     "scoped to the tenant that collected it, and is transmitted over HTTPS. No card or "
     "bank data is collected or stored, because no online payment gateway is integrated. "
     "All third-party libraries used are released under permissive open-source licences "
     "that allow academic and commercial use.", "Feasible"),
]

# =========================================================== CHAPTER 3 =======
CH3_SDLC = [
    "The iterative and incremental model has been selected for this project. In this model "
    "the system is built in a series of iterations, each of which passes through "
    "requirement analysis, design, implementation, testing and evaluation, and each of "
    "which delivers a working increment of the system (Sommerville, 2016).",

    "The model was chosen for three reasons specific to this project. First, the "
    "requirements of the seller dashboard are expected to be refined through repeated "
    "feedback from prospective sellers, and an iterative model allows that feedback to be "
    "absorbed without restarting the design. Second, the system decomposes naturally into "
    "increments that can be built and tested independently: the tenancy and authentication "
    "core, the catalogue and storefront, and finally the cart, order and administration "
    "modules. Third, the multi-tenant isolation logic is the highest-risk element of the "
    "design, and building it in the first iteration means it is exercised by every "
    "subsequent increment rather than being validated only at the end.",

    "A purely sequential waterfall model was rejected because it would defer all testing "
    "of tenant isolation until after the whole system was written, and an agile process "
    "with continuous customer involvement was rejected because the project has no "
    "permanently available product owner. Figure 1 shows the model as it will be applied.",
]

CH3_ARCHITECTURE = [
    "The system follows a three-tier architecture consisting of a presentation tier, an "
    "application tier and a data tier, shown in Figure 3. The tiers communicate only "
    "through defined interfaces, so that each can be developed and deployed separately.",

    "The presentation tier is a Next.js application that serves three kinds of page from "
    "one deployment: the public storefronts, the seller dashboard and the platform "
    "administration console. Every request first passes through tenant resolution "
    "middleware, which reads the HTTP Host header and looks up the corresponding store. A "
    "request for a platform subdomain such as a seller's store address, or for a verified "
    "custom domain, is resolved to that tenant and rewritten to the storefront routes; a "
    "request for the application subdomain is routed to the dashboard. Storefront pages "
    "are rendered on the server so that product pages are indexable by search engines, "
    "which is a functional requirement for sellers who depend on being found.",

    "The application tier is a FastAPI service that exposes a versioned REST interface. It "
    "is organised into service modules for authentication and access control, tenant and "
    "domain management, catalogue and inventory, cart and orders, and reporting. Every "
    "module reaches the database through a single data-access layer built on the "
    "SQLAlchemy ORM. That layer holds the tenancy logic: the tenant established for the "
    "request is stored in a request-scoped context, and every query against a "
    "tenant-owned table is filtered by it, so that isolation does not depend on each "
    "individual query being written correctly.",

    "The data tier is a single PostgreSQL database in which every tenant-owned table "
    "carries a tenant identifier column, supported by Redis for caching and session data "
    "and by object storage for product images. Row-level security policies in PostgreSQL "
    "provide a second line of defence behind the application-level scoping, so that a "
    "query that escapes the tenancy layer still cannot read another tenant's rows.",

    "A typical request illustrates the flow. A customer opens a storefront address; the "
    "presentation tier resolves the host to a tenant and requests that tenant's published "
    "products from the application tier over HTTPS; the application tier authorises the "
    "request, applies the tenant filter in the data-access layer, and queries PostgreSQL; "
    "the resulting rows are serialised as JSON, returned to the presentation tier, and "
    "rendered into HTML that is sent to the browser.",
]

CH3_ALGO_INTRO = (
    "Three parts of the system depend on logic that is not a simple create, read, update "
    "or delete operation. Each is described below as numbered steps."
)

ALGO_1_TITLE = "3.4.1 Tenant Resolution Algorithm"
ALGO_1_INTRO = (
    "This algorithm establishes which store a request belongs to. It runs before any other "
    "processing, in the presentation tier for page requests and in the application tier "
    "for interface requests."
)
ALGO_1_STEPS = [
    "Read the Host header of the incoming request and convert it to lower case, removing "
    "any port suffix.",
    "If the host equals the platform application domain, mark the request as a dashboard "
    "request, resolve the tenant from the authenticated user's active membership, and "
    "stop.",
    "If the host equals the platform root domain, mark the request as a marketing request "
    "with no tenant, and stop.",
    "If the host ends with the platform storefront suffix, extract the leading label as "
    "the store slug and look up the store with that slug.",
    "Otherwise, treat the host as a custom domain and look up a verified domain record "
    "with that host name.",
    "If no store is found, or the store status is not active, return a store-not-found "
    "response and stop.",
    "Store the identifier of the resolved tenant in the request-scoped context, load the "
    "theme settings for that tenant, and continue processing the request.",
]

ALGO_2_TITLE = "3.4.2 Cart Pricing and Discount Algorithm"
ALGO_2_INTRO = (
    "This algorithm computes the amount payable for a cart. It is executed whenever the "
    "cart changes and again at checkout, so that a price displayed to the customer is "
    "recomputed rather than trusted from the client."
)
ALGO_2_STEPS = [
    "Set the subtotal to zero.",
    "For each cart line, read the current price of the referenced variant, multiply it by "
    "the line quantity, store the result as the line total, and add it to the subtotal.",
    "If a discount code has been supplied, retrieve the discount belonging to the current "
    "tenant with that code; if it does not exist, has expired, or its minimum order value "
    "exceeds the subtotal, reject the code and set the discount amount to zero.",
    "If the discount is valid and of percentage type, set the discount amount to the "
    "subtotal multiplied by the percentage value, rounded to two decimal places; if it is "
    "of fixed type, set the discount amount to the lesser of the fixed value and the "
    "subtotal.",
    "Determine the shipping zone that contains the delivery address of the order, and read "
    "the rate defined for that zone; if no zone matches, apply the default rate of the "
    "store.",
    "Compute the total as the subtotal, minus the discount amount, plus the shipping rate.",
    "Return the subtotal, the discount amount, the shipping rate and the total, together "
    "with the reason for any rejected discount code.",
]

ALGO_3_TITLE = "3.4.3 Order Placement and Stock Reservation Algorithm"
ALGO_3_INTRO = (
    "This algorithm converts a cart into an order. It must not allow two customers to be "
    "sold the last unit of the same variant, so the stock check and the reservation are "
    "performed inside one database transaction."
)
ALGO_3_STEPS = [
    "Begin a database transaction.",
    "Re-read every cart line and lock the inventory row of each referenced variant for "
    "update.",
    "For each line whose variant is tracked, compare the requested quantity with the stock "
    "on hand minus the stock already reserved.",
    "If any line fails the comparison, roll back the transaction and return the cart to "
    "the customer with a stock conflict message identifying the affected lines.",
    "Recompute the cart totals using the algorithm in Section 3.4.2, so that the stored "
    "order reflects prices verified at the moment of placement.",
    "Create the order record with a generated order number, the resolved tenant, the "
    "customer, the delivery address, the computed totals, a status of pending and a "
    "payment method of cash on delivery.",
    "Create one order line for each cart line, copying the unit price into the line so "
    "that later price changes do not alter the order.",
    "Increase the reserved quantity of each tracked variant by the ordered quantity.",
    "Mark the cart as converted, commit the transaction, and queue notifications to the "
    "seller and the customer.",
]

CH3_FLOWCHART = [
    "Figure 4 shows the sequence of operations performed by the system from the moment a "
    "visitor opens a storefront address to the moment an order is confirmed. The chart is "
    "divided into three stages, connected by the numbered off-page connectors.",

    "Stage A resolves the store and serves the catalogue. The middleware extracts the Host "
    "header and applies the tenant resolution algorithm of Section 3.4.1; if no active "
    "store matches, the visitor is shown a store-not-found page and the flow ends. "
    "Otherwise the tenant context and theme are loaded and the catalogue for that tenant "
    "is rendered. When the customer adds an item, the system checks that the chosen "
    "variant is in stock before creating or updating the cart line, and the customer may "
    "continue browsing or proceed to checkout.",

    "Stage B collects the information needed to complete the order and computes the amount "
    "payable. A customer who is not authenticated supplies contact details as a guest. The "
    "shipping address is collected, and the totals are computed by the algorithm of "
    "Section 3.4.2; an invalid discount code is rejected and the totals are recomputed "
    "before the order summary is confirmed.",

    "Stage C creates the order. The stock check of Section 3.4.3 is repeated at this "
    "point, because stock may have changed while the customer was completing the checkout. "
    "If it fails, the customer is returned to the cart through connector 3. If it "
    "succeeds, the order is created and inventory is reserved in one transaction, the "
    "payment method is recorded as cash on delivery, the seller and customer are notified, "
    "and the confirmation is displayed.",
]

CH3_USECASE = [
    "The use case diagram in Figure 5 shows the interactions between the actors and the "
    "system. Five actors are involved. The platform administrator approves and suspends "
    "stores and monitors platform-wide activity. The store owner creates and configures a "
    "store, maps its subdomain and custom domain, customises the storefront theme, defines "
    "discounts and shipping zones, manages staff and roles, and views sales reports. Store "
    "staff manage the product catalogue and its variants, maintain inventory levels, and "
    "process and fulfil orders. The registered customer creates a customer account, "
    "browses and searches the storefront, manages a shopping cart, places orders and "
    "tracks their status. The guest visitor may browse, manage a cart and place an order "
    "without creating an account.",

    "As shown in Figure 5, the system supports 17 primary use cases across five actor "
    "roles. Registration and authentication is shared between the platform administrator "
    "and the store owner, because both are platform users; storefront customers "
    "authenticate separately through the customer account use case, since customer "
    "accounts belong to a single tenant rather than to the platform.",
]

CH3_DFD0 = [
    "The context diagram in Figure 6 represents the whole platform as a single process and "
    "shows the data that crosses its boundary. Four external entities interact with the "
    "system. The store owner supplies store details, product data, and discount and "
    "shipping rules, and receives the store dashboard, sales reports and order alerts. "
    "Store staff supply stock updates and fulfilment status, and receive the order queue "
    "and inventory alerts. The customer supplies search terms, cart items and order and "
    "address details, and receives product listings, cart summaries and order status. The "
    "platform administrator supplies store approval decisions and platform settings, and "
    "receives the store registry and a platform activity summary."
]

CH3_DFD1 = [
    "Figure 7 decomposes the single process of Figure 6 into six processes and six data "
    "stores. Process 1.0, Manage Users and Access, authenticates platform users and issues "
    "session tokens against the user and role store. Process 2.0, Provision Store and "
    "Domain, creates tenant records and domain mappings and applies the administrator's "
    "approval decisions. Process 3.0, Manage Catalog and Inventory, maintains products, "
    "variants and stock levels. Process 4.0, Serve Storefront and Cart, resolves the "
    "tenant, reads the catalogue and maintains cart records for storefront visitors. "
    "Process 5.0, Process Order, converts a cart into an order, reserves stock, records the "
    "customer, and reports fulfilment progress. Process 6.0, Generate Reports, reads order "
    "and catalogue data to produce sales reports for sellers and an activity summary for "
    "administrators.",

    "The data stores mirror the entity groups of Section 3.8: D1 holds users and roles, D2 "
    "tenants and domains, D3 products and inventory, D4 carts, D5 orders and D6 storefront "
    "customers. Every store except D1 is partitioned internally by tenant identifier.",
]

CH3_ERD = [
    "The entity relationship diagram in Figure 8 shows the principal entities of the "
    "database, their primary and foreign keys and the cardinality of each relationship. "
    "TENANT is the root of the tenant-owned data: a tenant has many domains, products, "
    "collections, customers, carts, orders, discounts and shipping zones, and every one of "
    "those tables carries tenant_id as a foreign key referencing TENANT. Platform users "
    "are held separately in USER and are connected to tenants through MEMBERSHIP, which "
    "carries the role held by that user in that tenant; this allows one person to hold "
    "different roles in different stores.",

    "In the catalogue, a PRODUCT has many PRODUCT_VARIANT rows, each identified by a "
    "unique SKU and carrying its own price, and each variant has exactly one "
    "INVENTORY_ITEM recording stock on hand and stock reserved. Products are grouped into "
    "collections through a many-to-many association. In the commerce path, a CUSTOMER "
    "saves many addresses and owns carts and orders; a CART contains many CART_ITEM rows "
    "and an ORDERS row contains many ORDER_ITEM rows, each referring to a variant and "
    "storing the unit price agreed at the time. An order also references the address it "
    "ships to, the discount applied and the shipping zone that priced it.",

    "Supporting tables that are not drawn in Figure 8, in order to keep the diagram "
    "legible, are the theme settings of a store, product media assets, shipment tracking "
    "records and the platform-level role definitions. Each follows the same rule as the "
    "entities shown: it carries tenant_id where it is tenant-owned, and its primary key is "
    "a universally unique identifier.",
]

# =========================================================== CHAPTER 4 =======
CH4_INTRO = (
    "This chapter describes how the project will be implemented. Since the project is "
    "still at the proposal stage, no implementation or testing results are reported here."
)

TABLE5_ROWS = [
    ("Processor", "Intel Core i5 (8th generation) or equivalent",
     "Running the development environment and local services"),
    ("RAM", "Minimum 8 GB, 16 GB recommended",
     "Running the database, application server and front-end build concurrently"),
    ("Storage", "Minimum 40 GB free, solid-state drive",
     "Source code, dependencies, container images and the local database"),
    ("Operating system", "Windows 10 or 11, or Ubuntu 22.04 LTS",
     "Development platform"),
    ("Code editor", "Visual Studio Code", "Development environment"),
    ("Database server", "PostgreSQL 16", "Local and deployed relational data storage"),
    ("Cache server", "Redis 7", "Session data and cached storefront responses"),
    ("Containerisation", "Docker and Docker Compose",
     "Reproducible local environment for the database and cache"),
    ("Browser", "Google Chrome and Mozilla Firefox, current versions",
     "Front-end development and testing"),
    ("API testing tool", "Postman and the built-in OpenAPI documentation",
     "Manual and exploratory testing of the interface"),
    ("Diagramming", "draw.io and Mermaid", "System design diagrams"),
    ("Version control", "Git and GitHub", "Source code management and collaboration"),
]

TABLE6_ROWS = [
    ("Programming languages", "Python 3.11 and TypeScript"),
    ("Front end", "Next.js 15 (React), Tailwind CSS"),
    ("Back end and framework", "FastAPI with Pydantic and Uvicorn"),
    ("Database", "PostgreSQL 16"),
    ("Object-relational mapping", "SQLAlchemy 2.0 with Alembic migrations"),
    ("Cache and sessions", "Redis 7"),
    ("Object storage", "S3-compatible storage for product media"),
    ("Authentication", "JSON Web Tokens with Argon2 password hashing"),
    ("Testing", "pytest for the back end, Playwright for end-to-end tests"),
    ("Development environment", "Visual Studio Code, Docker Compose"),
    ("Version control", "Git and GitHub"),
    ("Deployment platform", "Vercel for the front end, Render for the API and database"),
]

CH4_JUSTIFICATION = [
    "FastAPI was selected for the application tier because it validates every request and "
    "response against declared Pydantic models and generates OpenAPI documentation from "
    "those models automatically (Ramírez, 2024). In a multi-tenant system where three "
    "different clients consume the same interface, an interface contract that cannot drift "
    "from the code is a direct benefit. Its asynchronous request handling also suits a "
    "workload dominated by database waits. Django was considered, since it offers a "
    "built-in administration interface, but its session-based, single-tenant conventions "
    "would have to be worked against rather than with.",

    "Next.js was selected for the presentation tier for two specific reasons. First, its "
    "middleware runs before routing and can rewrite a request based on the Host header, "
    "which is exactly the mechanism required to serve many storefronts and two "
    "applications from one deployment (Vercel, 2024). Second, its server-side rendering "
    "produces complete HTML for storefront pages, which a purely client-rendered "
    "application would not, and search engine visibility is a stated requirement of the "
    "sellers this project serves.",

    "PostgreSQL was chosen over MySQL because the tenancy design depends on features that "
    "PostgreSQL provides directly: row-level security policies give a database-level "
    "guarantee of tenant isolation behind the application-level filter, and JSONB columns "
    "allow variant option sets and theme settings to be stored without a separate table "
    "for every attribute (PostgreSQL Global Development Group, 2024).",

    "SQLAlchemy with Alembic was chosen because the tenancy filter can be implemented once, "
    "in the session and query layer, and applied to every tenant-owned model, rather than "
    "being repeated in each query (SQLAlchemy Project, 2024). Alembic keeps the schema "
    "under version control alongside the code, which is required by the maintainability "
    "requirement in Table 2. Argon2 was chosen for password hashing over older algorithms "
    "because it is the current recommendation for password storage in the OWASP guidance "
    "(Open Web Application Security Project, 2021).",
]

CH4_STRUCTURE_INTRO = (
    "The repository layout, testing approach and version control practice are described "
    "below."
)

CH4_APPROACH_ITEMS = [
    ("Project structure",
     "the system is held in two repositories. The back-end repository contains app/ "
     "(api/, core/, models/, schemas/, services/), alembic/ for migrations, tests/ and "
     "docs/. The front-end repository contains src/app/ with separate route groups for the "
     "storefront, the seller dashboard and the platform console, src/components/, "
     "src/lib/ and the tenant resolution middleware."),
    ("Unit testing",
     "each service module is tested in isolation with pytest, using a transactional test "
     "database. Pricing, discount and stock reservation logic are covered by table-driven "
     "cases including boundary values such as a zero-stock variant and an expired discount "
     "code."),
    ("Integration testing",
     "the interface is exercised end to end against a live test database, covering "
     "registration, store provisioning, catalogue creation, cart operations and order "
     "placement. A dedicated group of integration tests creates two tenants and asserts "
     "that every read and write operation performed under one tenant's credentials fails "
     "or returns empty for the other tenant's data."),
    ("User acceptance testing",
     "a small group of prospective sellers and customers will be asked to complete defined "
     "tasks, such as creating a store, publishing a product and placing an order, and the "
     "outcome of each task will be recorded."),
    ("Test case documentation",
     "test cases are recorded in a table with the columns test case identifier, module, "
     "precondition, input, expected output, actual result and status. The 40 test cases "
     "named in the third specific objective are distributed across authentication and "
     "access control, tenant isolation, catalogue and inventory, cart and pricing, order "
     "placement, and storefront routing."),
    ("Version control",
     "all source code and design documents are maintained in Git from the start of the "
     "project, with a branch for each feature and a review before merging. Migrations are "
     "committed together with the code that requires them."),
]

# =========================================================== CHAPTER 5 =======
CH5_INTRO = (
    "This chapter describes the anticipated results and benefits of the proposed project. "
    "Everything stated here is an expectation to be verified during testing, not a result "
    "already obtained."
)

CH5_DELIVERABLES = [
    "A deployed multi-tenant web application in which a seller can register, create a "
    "store, publish a catalogue and receive orders, and in which a customer can browse a "
    "storefront and place an order using cash on delivery.",
    "A seller dashboard for catalogue, inventory, discount, shipping, staff and order "
    "management, and a platform administration console for approving and suspending "
    "stores.",
    "Server-rendered storefronts reachable at platform subdomains and at verified custom "
    "domains, each rendering only the catalogue and theme of its own tenant.",
    "The complete source code of the back-end and front-end applications, together with "
    "setup instructions, interface documentation generated from the code, and the design "
    "documents produced in Chapter 3.",
    "The database schema as a versioned sequence of migrations, together with a seed "
    "dataset of sample stores, products and orders for demonstration.",
    "A documented test suite and a completed test case table recording the outcome of each "
    "of the defined test cases, including the cross-tenant isolation cases.",
    "The Git repositories containing all code, migrations and documentation, with the "
    "history of the project preserved.",
]

CH5_BENEFITS = [
    "The completed system is expected to allow an independent seller to move from a social "
    "media page to a branded storefront without technical assistance. Because store "
    "provisioning is self-service, the steps that currently require a developer, namely "
    "obtaining hosting, installing a commerce package and configuring a domain, are "
    "expected to be replaced by a registration form and a domain verification step.",

    "The system is expected to remove the manual order book described in Section 1.2. "
    "Orders will be recorded with a generated order number, a stored delivery address, the "
    "prices agreed at the time of purchase and an explicit status, so that the duplication "
    "and loss of orders that arises from tracking sales in chat threads is eliminated. "
    "This expectation will be verified during user acceptance testing by asking sellers to "
    "complete a defined set of order-handling tasks and recording the outcome.",

    "Because stock is reserved inside the same transaction that creates the order, the "
    "system is expected to prevent the sale of items that are no longer available, which "
    "the current manual process cannot detect until the seller attempts to dispatch the "
    "goods.",

    "For customers, the expected benefit is a storefront that shows accurate availability, "
    "a consistent price including delivery charges, and an order status that can be checked "
    "without contacting the seller.",

    "For the platform operator, the expected benefit of the shared-database multi-tenant "
    "design is that the marginal cost of an additional seller is the cost of the rows that "
    "seller creates, rather than the cost of a further deployment, which is what makes an "
    "affordable service for single-shop retailers possible.",

    "The seller is also expected to gain visibility that a social media page cannot "
    "provide. Because storefront pages are rendered on the server and served from a "
    "domain the seller controls, product pages are expected to be indexable by search "
    "engines, so that a customer searching for a product can reach the seller's store "
    "directly rather than only through a social media feed.",

    "Finally, the project is expected to produce a documented reference implementation of "
    "shared-schema multi-tenancy in a Python and TypeScript stack, including the tenancy "
    "layer and the isolation test cases, which may be reused by later projects addressing "
    "similar problems.",
]

# --------------------------------------------------------------- references --
REFERENCES = [
    "Adobe. (2024). *Adobe Commerce developer documentation* [Computer software "
    "documentation]. https://developer.adobe.com/commerce/docs/",

    "Bezemer, C.-P., & Zaidman, A. (2010). Multi-tenant SaaS applications: Maintenance "
    "dream or nightmare? In *Proceedings of the Joint ERCIM Workshop on Software Evolution "
    "and International Workshop on Principles of Software Evolution* (pp. 88–92). "
    "Association for Computing Machinery. https://doi.org/10.1145/1862372.1862393",

    "Chong, F., & Carraro, G. (2006). *Architecture strategies for catching the long tail*. "
    "Microsoft Corporation. "
    "https://learn.microsoft.com/en-us/previous-versions/dotnet/articles/aa479069(v=msdn.10)",

    "Codd, E. F. (1970). A relational model of data for large shared data banks. "
    "*Communications of the ACM, 13*(6), 377–387. https://doi.org/10.1145/362384.362685",

    "Fielding, R. T. (2000). *Architectural styles and the design of network-based software "
    "architectures* [Doctoral dissertation, University of California, Irvine]. "
    "https://ics.uci.edu/~fielding/pubs/dissertation/top.htm",

    "International Trade Administration. (2024). *Nepal country commercial guide: "
    "eCommerce*. U.S. Department of Commerce. "
    "https://www.trade.gov/country-commercial-guides/nepal-ecommerce",

    "Krebs, R., Momm, C., & Kounev, S. (2012). Architectural concerns in multi-tenant SaaS "
    "applications. In *Proceedings of the 2nd International Conference on Cloud Computing "
    "and Services Science* (pp. 426–431). SciTePress. "
    "https://doi.org/10.5220/0003957604260431",

    "Medusa. (2024). *Medusa documentation* [Computer software documentation]. "
    "https://docs.medusajs.com/",

    "Open Web Application Security Project. (2021). *OWASP Top 10:2021*. "
    "https://owasp.org/Top10/",

    "PostgreSQL Global Development Group. (2024). *PostgreSQL 16 documentation* [Computer "
    "software documentation]. https://www.postgresql.org/docs/16/",

    "Ramírez, S. (2024). *FastAPI documentation* (Version 0.115) [Computer software "
    "documentation]. https://fastapi.tiangolo.com/",

    "Saleor Commerce. (2024). *Saleor documentation* [Computer software documentation]. "
    "https://docs.saleor.io/",

    "Shopify. (2024). *Shopify developer documentation* [Computer software documentation]. "
    "https://shopify.dev/docs",

    "Sommerville, I. (2016). *Software engineering* (10th ed.). Pearson.",

    "SQLAlchemy Project. (2024). *SQLAlchemy 2.0 documentation* [Computer software "
    "documentation]. https://docs.sqlalchemy.org/en/20/",

    "Vercel. (2024). *Next.js documentation* (Version 15) [Computer software "
    "documentation]. https://nextjs.org/docs",

    "Wix.com. (2024). *Wix eCommerce developer documentation* [Computer software "
    "documentation]. https://dev.wix.com/docs",

    "WooCommerce. (2024). *WooCommerce documentation* [Computer software documentation]. "
    "https://woocommerce.com/documentation/",
]

# ------------------------------------------------------------------ timeline --
# activity, list of month indices (0-based) that are shaded
TIMELINE = [
    ("Requirement analysis and literature review", [0, 1]),
    ("System design (architecture, DFD, ER, use case)", [1, 2]),
    ("Database design and setup", [2]),
    ("Core module development (tenancy, authentication, catalogue)", [2, 3]),
    ("Storefront, cart and order module development", [3, 4]),
    ("Integration of modules", [4]),
    ("Testing (unit, integration, user acceptance)", [4, 5]),
    ("Deployment", [5]),
    ("Documentation and report writing", [0, 1, 2, 3, 4, 5]),
]
