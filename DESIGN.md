# Design Decisions

> [!NOTE]  
> Return back to the [README.md](README.md) file.

### Design Approach

The design process for the Frank Moth website involved more than developing a visual identity. It required careful consideration of how to organise a substantial body of artistic and professional content, accommodate different visitor needs and create a cohesive experience across the website's various sections. One of the main challenges was presenting Frank Moth's extensive and varied content in a way that was both accessible and engaging.

The artwork archive formed the foundation of the project, with collections providing a structured way to explore the artists' work and individual artwork pages allowing each piece to be presented in greater detail. Beyond the archive, the website also needed to communicate the artists' identity, creative background and professional achievements. The About, In Situ and Collaborations pages were designed to complement one another, presenting their story, artistic practice, work in real-world settings, professional partnerships and recognition through exhibitions, interviews and other media coverage.

Another important consideration was accommodating the website's different purposes and the journeys visitors might take. While some visitors come primarily to explore the artwork, others may be interested in learning about the artists, discovering professional collaborations, purchasing existing products or commissioning a personalised piece. These different interests informed the organisation of the website into distinct but interconnected sections. Given the breadth of content, I chose to design the homepage as a visual index of the entire website, offering a carefully structured introduction to its main areas. Rather than functioning solely as a landing page, it provides visitors with a preview of the different types of content and clear opportunities to continue exploring according to their interests.

The visual design of the Frank Moth website was guided by the artists' established aesthetic and the distinctive character of their artwork. Rather than introducing an entirely new visual identity, I chose to build upon the typography, colours and minimalist style of their existing website, respecting their preferences while adapting these elements to the expanded functionality and content of the new application.

Frank Moth's digital collages are often rich in colour, intricate details and striking visual contrasts. To complement this, I adopted a restrained approach to the surrounding interface, allowing the artwork itself to provide the primary visual impact. Background colours, decorative elements and interface controls were intentionally kept subtle, creating a clean presentation that supports the imagery without competing for attention.

Two closely related, light neutral background colours were used throughout the website to create a gentle visual rhythm and distinguish adjacent sections without relying on prominent borders or additional decorative elements. The artists' existing bright green accent colour was retained but applied selectively to small details, interactive states and visual highlights. A dark navy blue was also introduced to provide additional contrast and variation, while maintaining the overall restrained appearance.

Small, recurring details, such as pairs of bright green dots and subtle green underlines, were introduced as visual motifs throughout the website. Their repetition creates a sense of continuity and adds occasional pops of colour to the restrained interface, reinforcing the artists' established visual identity without distracting from the artwork.

Subtle box shadows were used throughout the website to introduce a sense of depth and prevent the minimalist interface from appearing overly flat. Their restrained application creates a gentle three-dimensional effect around images and other elements, while also helping define boundaries between the navigation bar, footer, form fields and surrounding content. This approach provides visual separation without relying on prominent borders or decorative elements that might distract from the artwork.

Typography plays a particularly important role in establishing the website's character. Unlike text-heavy applications, the Frank Moth portfolio relies primarily on imagery, headings, short descriptions and editorial-style statements rather than extensive paragraphs. This allowed greater emphasis on expressive typography, with two contrasting display fonts used to establish hierarchy, distinguish different types of content and create rhythm between consecutive text elements. A third, more restrained font supports the relatively limited body text, maintaining readability without compromising the overall aesthetic.

The same principles were applied to interactive components, including forms, navigation elements and artwork galleries. Minimal styling, carefully controlled spacing and subtle visual feedback were used to maintain consistency across the interface, while ensuring that functional elements remain clear and accessible. 

Social media links were intentionally placed in the footer rather than the main navigation or other prominent areas of the website. Although Frank Moth maintain a presence across several social platforms, the primary purpose of the website is to showcase their artwork and guide visitors towards relevant content and services. Keeping these links in a more discreet location ensures that they remain easily accessible without competing with the portfolio, navigation and primary calls to action for visitors' attention. The resulting design aims to combine the artists' established visual identity with a cohesive, contemporary interface suited to both artistic exploration and practical interactions.


### Shared Layout and Navigation

#### Navigation Bar

The navigation bar was designed to provide clear and consistent access to the website's main sections. The Frank Moth name is positioned on the left and acts as a link to the homepage, while the main navigation links — Art, About, In Situ, Collaborations, Commissions and Where to Buy — are arranged on the right. Active-page styling uses an underline and a bright green dot to help visitors identify their current location within the website. The hover effect repeats these visual elements, with additional movement to provide interactive feedback while maintaining consistency between navigation states. Given the number of sections and the length of several pages, the navigation bar remains sticky at the top of the screen, allowing visitors to move between sections without having to scroll back to the beginning.

On smaller screens, the navigation collapses into a hamburger menu to accommodate the number of links without overcrowding the available space. The active-page styling is retained within the expanded mobile menu, maintaining visual orientation across screen sizes. The available space beside the hamburger menu is used to keep the account icon permanently visible, providing convenient access to login, registration and account options without requiring visitors to open the main navigation.

The account controls also adapt to the user's authentication status and permissions. The account icon changes appearance depending on whether the visitor is logged in, while its dropdown presents the appropriate options. Authenticated users are additionally provided with a dedicated navigation link to **My Account** or the **Artist Dashboard**, depending on their permissions. This allows regular visitors to access their personal features while giving the artists direct access to the tools needed to manage the website, without exposing administrative navigation to other users.

To further support navigation on longer pages, **Back to Top** buttons provide a convenient way to return to the beginning of the page without excessive scrolling. Together with the sticky navigation bar, they help visitors move efficiently through the website's extensive visual content.

#### Footer

The footer was designed to remain minimal and unobtrusive, appearing at the bottom of each page rather than occupying a permanent position on the screen. It provides consistent access to Frank Moth's social media profiles, which were deliberately placed in the footer rather than the main navigation or page content. This keeps the links accessible throughout the website without allowing them to compete with the artwork and other primary content for visitors' attention.

A link to the Contact page is also included in the footer. Given the number of sections already present in the main navigation, I chose to prioritise the artwork, creative projects and services there, while keeping contact information easily accessible through the footer. The Contact page is also linked from relevant sections throughout the website, including the homepage and pages presenting the artists' work and collaborations. This approach provides multiple opportunities for visitors to get in touch when appropriate, without overcrowding the navigation bar.



### Page-by-Page Design Analysis

#### Home Page

The homepage was designed to function as a visual index of the website, introducing its different areas while maintaining a cohesive and engaging experience. With so much varied content to represent, the main challenge was to create a sequence of relatively compact sections that would provide meaningful previews without overwhelming visitors. Alternating light neutral backgrounds, subtle horizontal dividers and carefully balanced spacing establish a visual rhythm, helping distinguish the sections while allowing the colourful artwork to remain the focus. I also chose more expressive, editorial-style headings for the homepage, such as *Inside Frank Moth's World* and *Something Personal, Something to Keep*, while retaining clear, descriptive labels in the main navigation and corresponding links. This combination introduces personality without compromising clarity or ease of navigation.

The opening hero features a video of Frank Moth's monumental staircase installation in Blois, France. I selected this particular piece because it communicates several aspects of the artists' work at once: their distinctive surreal imagery, the scale and versatility of their creative practice, and their experience with ambitious international projects. It establishes credibility and creates a strong first impression without requiring extensive introductory text. The video plays automatically without sound and includes a pause control, allowing visitors to stop the motion if they prefer. Its relatively gentle movement gives it the quality of a living artwork, reinforced by a surrounding frame on larger screens.

The **Inside Frank Moth's World** section introduces the artwork archive through a carousel of twelve selected pieces. Rather than displaying only one or two representative images, I chose a carousel to offer a broader impression of the artists' varied compositions while keeping the section relatively compact. Visitors can explore the selection at their own pace before following the link to the Art page, where the complete archive is organised into collections. The carousel's minimal controls and restrained presentation keep attention on the artwork itself.

The **Meet Frank Moth** section provides a brief introduction to the artists and their creative approach, accompanied by a link to the About page. Incorporating short editorial statements between the more image-heavy sections helps vary the composition and gives visitors an opportunity to learn about the people and ideas behind the artwork. The text remains intentionally concise, offering context without interrupting the homepage's visual flow or duplicating the more detailed information available on the About page.

The **Art Beyond the Frame** section introduces the different contexts in which Frank Moth's work appears beyond individual digital compositions. The extensive photographic material from the original website was reorganised into two distinct categories: **In Situ**, showing artwork displayed in real environments, and **Creative Partnerships**, presenting professional collaborations and commissioned projects. Representative images provide an immediate understanding of these different applications of the artists' work, while dedicated links allow visitors to explore each area in greater detail.

The **Something Personal, Something to Keep** section shifts the focus towards opportunities to own or commission Frank Moth artwork. Since purchasing existing products and requesting a personalised commission represent different visitor intentions, I chose to introduce them together while providing separate paths to the relevant pages. Visitors can explore the new commission service or continue to Where to Buy, which presents the retailers offering the artists' work and related products. This maintains a clear distinction between the two purchasing experiences without making the homepage feel overly commercial.

Finally, the **Stay Connected** section provides opportunities for further engagement through the artists' substack and direct communication. Positioned towards the end of the homepage, it offers a natural conclusion to the progression from discovering the artwork and learning about the artists to exploring their professional work and purchasing opportunities. Its placement makes these additional forms of engagement readily available without competing with the primary content earlier on the page.


#### Art

The Art section was designed to make Frank Moth's extensive artwork archive easy to navigate while maintaining a minimal, image-focused presentation. Rather than displaying all artworks in a single continuous gallery, the content is organised into three levels: a collections overview, individual collection galleries and dedicated artwork detail pages. This structure allows visitors to explore the artists' work progressively, moving from a broad overview of their collections to individual pieces, while keeping the browsing experience clear, manageable and visually engaging.

##### Art Page

The Art Page was designed as a collections overview to introduce Frank Moth's artwork archive in a simple, visually engaging format that encourages visitors to explore the individual collections. Rather than presenting a conventional grid of thumbnails, I chose an alternating image-and-text layout, with a representative artwork displayed alongside each collection's title, a short description provided by the artists and a link to explore the collection.

The arrangement alternates between image and text from one row to the next, creating a gentle visual rhythm and adding variety to the page without introducing unnecessary decorative elements. The representative images offer an immediate impression of each collection's character, while the accompanying descriptions provide context and help visitors decide which collections interest them. Generous spacing and restrained styling allow each collection to stand out individually, keeping the artwork as the main visual focus while maintaining a consistent and easy-to-follow browsing experience. On mobile screens, the image and text sections stack vertically, with the representative artwork appearing first, followed by the collection's title, description and link. This preserves the visual introduction to each collection while making the content easier to follow on narrower screens.


##### Artworks Page

The Artworks page was designed to recreate the experience of browsing an art gallery, allowing visitors to focus entirely on the visual qualities of Frank Moth's work. Given the richness of colour, detail and composition in the artworks, I chose a simple grid against a light neutral background, with generous spacing between images and minimal surrounding interface elements. Artwork titles, dates and descriptions were deliberately omitted from this view to avoid visual distractions and allow visitors to appreciate the collection as a whole. This information is instead presented on dedicated Artwork Detail pages, accessible by selecting an individual image. A subtle hover effect, combining a slight upward movement with a more pronounced shadow, was intentionally introduced to indicate that the images are interactive without distracting from the artwork or disrupting the gallery's minimalist appearance. The gallery uses a responsive grid, displaying four artwork columns on larger screens, three on medium-sized screens and two on mobile devices. I deliberately retained two columns on smaller screens rather than switching to a single-column layout, allowing visitors to see several artworks together and preserving the immersive experience of browsing a collection while adapting to the available screen width.

Pagination was introduced to prevent visitors from having to navigate excessively long pages, particularly in collections containing a large number of artworks. I chose to display **24 artworks per page** as a balance between visual immersion and manageable browsing. A smaller number would interrupt the experience with frequent page changes, while displaying an entire collection at once could result in an overwhelming amount of content and unnecessarily long scrolling. The selected page size allows visitors to spend time exploring a substantial selection of artworks, including on larger screens, while keeping the experience manageable on mobile devices.


##### Artwork Detail Page

The Artwork Detail page was introduced to address an important limitation of Frank Moth's original website, where visitors could browse the artwork but could not open individual pieces for closer examination or access their titles and descriptions. I considered this an essential addition, allowing visitors to appreciate the intricate details of each composition through a larger, dedicated image presentation. The accompanying title, year and description provide further context and contribute to the artwork's identity. Frank Moth's titles and descriptions are often poetic and unconventional rather than purely factual, forming part of the artists' creative expression and complementing the visual narratives of their collages.

The page also plays an important role in connecting artistic exploration with purchasing opportunities. Allowing visitors to examine an individual artwork in greater detail supports more informed purchasing decisions, particularly for large-format prints and other decorative products. To simplify the purchasing journey, links to external retailers are provided, including a direct link to the specific artwork in Frank Moth's official Etsy shop where available. This addresses another limitation of the original website, where visitors had to navigate separately to a retailer and attempt to locate the artwork themselves. Authenticated users can also save artworks to their favourites for later consideration, supporting visitors who may wish to compare pieces or take more time before deciding on a purchase. A dedicated **Back to Collection** link allows visitors to return easily to the gallery they were exploring, maintaining a clear and intuitive browsing journey.

The layout was designed to balance the prominence of the artwork with the amount of accompanying information. On larger screens, the image occupies the left side of the page, while the title, description and purchasing options are grouped on the right. Since some artworks have lengthy titles and descriptions, this area can become relatively text-heavy. To introduce visual variety, the recurring pair of bright green dots was incorporated into the description with a hanging indentation, breaking up the continuous left alignment and creating a more distinctive editorial rhythm. This subtle detail reinforces the website's visual identity while maintaining a restrained composition that keeps the artwork itself as the primary focus. On smaller screens, the two-column layout becomes a single-column arrangement, with the artwork displayed first and the title, description and purchasing options stacked beneath it. This preserves the emphasis on the image while keeping the accompanying information readable and accessible on mobile devices.

### About Page

The About page was designed to offer visitors a brief glimpse into the people and creative identity behind Frank Moth, rather than a conventional, detailed artist biography. The artists have deliberately maintained a degree of anonymity, and I wanted the page to respect this aspect of their identity. The introductory photograph reflects this approach, showing the two artists with their faces largely obscured, while oversized Frank Moth typography dominates the composition. This creates a personal yet understated introduction, placing greater emphasis on their shared artistic identity than on the individuals themselves. A short biographical statement introduces their origins and the creation of Frank Moth, followed by a simple visual representation of their geographical journey together.

The page also introduces visitors to the artists' creative expression beyond their digital collages. A prominent section dedicated to their Substack publication, *Small Notes on Life and Art*, provides a direct link to their writing and offers another perspective on their artistic identity. The following statement about their distinctive style and approach to collage adds further context without overwhelming visitors with extensive explanations. Alternating neutral backgrounds, together with a narrow navy band featuring bright green typography, create visual separation between the sections while maintaining the website's established design language.

The lower part of the page presents the artists' professional achievements through three clearly organised columns: **Media Recognition & Publications**, **Interviews** and **Exhibitions**. These sections demonstrate the recognition and experience Frank Moth have gained over the years, adding credibility without adopting an overly promotional tone. The information is presented in simple typographic lists, with underlined links to external sources where available, allowing interested visitors to explore further. This restrained presentation keeps the page informative and easy to navigate while preserving its overall purpose: offering a meaningful introduction to the artists without revealing more than they have chosen to share.


### In Situ & Collaborations Pages

The In Situ and Collaborations pages were designed to showcase Frank Moth's artwork beyond their main collections, demonstrating how their creations become part of physical environments and are applied across different media. The two pages are connected through the contrasting concepts of *In Situ* (artwork in place) and *In Motu* (artwork in motion), a playful distinction that reflects the different ways their work exists beyond the digital gallery. In Situ focuses on artwork displayed within interiors and architectural spaces, while Collaborations presents its application to publications, printed materials, digital projects and other creative formats. Despite their different content, both pages share a consistent visual approach, using masonry-style galleries with large photographs, informative captions and restrained neutral backgrounds. This allows the colourful artwork to remain the main focus while giving visitors a broader understanding of its versatility and real-world impact. Both pages also include a Back to Top button, allowing visitors to return easily to the beginning of the galleries after exploring their extensive visual content.

#### In Situ

The In Situ page uses a responsive masonry gallery, displaying photographs in a single column on mobile screens and two columns from tablet-sized screens upwards. This allows the images to remain large enough to appreciate the artwork within its surroundings, while accommodating photographs of different proportions without cropping them into uniform shapes. The expressive heading *Our Art in the Wild* introduces the gallery in a playful, artistic tone, while the large photographs and understated background keep attention on the artwork and its relationship with the physical environment.

At the bottom of the page, an invitation encourages visitors who have purchased Frank Moth designs to share photographs of how they display them, either by using the suggested social media hashtag or through a link to the Contact page. This creates an opportunity for visitors to engage with the artists and potentially contribute to the growing collection of real-world examples.

#### Collaborations — In Motu

The Collaborations page was designed to showcase the variety of formats and creative projects in which Frank Moth's artwork has been featured, from publications and album covers to printed materials and digital projects. A masonry gallery allows images of different proportions to retain their natural dimensions, while captions provide context for each project. Compared with the more spacious In Situ gallery, the denser arrangement reflects the diversity of applications while maintaining the same minimal, image-focused presentation.

A separate section presents a list of selected clients in a compact, understated typographic format, providing an overview of the artists' professional experience without competing with the gallery. Some entries link directly to the clients or related projects, allowing interested visitors to explore further. An invitation to collaborate, accompanied by a direct link to the Contact page, connects the artists' previous work with opportunities for future projects.

The responsive layout was designed with particular attention to visitors interested in commissioning or collaborating with the artists. On mobile screens, the selected clients list and contact invitation appear before the gallery, allowing visitors to quickly assess the artists' experience and get in touch without scrolling through the entire visual portfolio. From tablet-sized screens upwards, the clients list is positioned alongside the gallery, which uses a two-column masonry arrangement. On larger desktop screens, the gallery expands to three columns, making fuller use of the available space while keeping the clients list accessible. This approach prioritises relevant information on smaller devices without compromising the visual presentation of the artwork.


### Commissions Page

The Commissions page introduces a new service that was not available on Frank Moth's previous website, allowing visitors to commission bespoke artwork created specifically for them. The design aims to make this process feel creative, personal and enjoyable, rather than like a conventional order form.

A colourful hero section introduces the service and encourages visitors to explore the possibilities of commissioning original artwork. A collage of Frank Moth's existing works provides visual inspiration, while a gradient overlay ensures the introductory text remains readable.

The form offers two distinct creative approaches. **Give Form to a Thought** allows visitors to share their ideas and guide the artists through their preferences, including moods, colours, imagery and artwork format. Alternatively, **Let Us Surprise You** gives the artists greater creative freedom, allowing visitors to bypass the preference selections and proceed directly to choosing the artwork format. This approach accommodates both visitors with a specific vision and those who prefer to leave the creative direction to the artists.

The form uses a restrained visual design to keep attention on the creative choices without unnecessary decoration. A subtle background pattern and clearly separated sections establish a visual rhythm, making the longer form easier to navigate. Interactive selections provide immediate visual feedback: selected options remain highlighted, while unavailable options become visually muted and inactive. Visitors can select up to two moods and two colours, or one imagery style and artwork format. Once a selection limit is reached, the remaining options are disabled until an existing choice is deselected. The form also responds to earlier decisions; for example, choosing a digital artwork format disables the physical size options. These interactions communicate available choices and constraints directly through the interface, reducing confusion and avoiding unnecessary validation errors.

The responsive layout adapts the arrangement of the form to different screen sizes. On larger screens, options are displayed in multi-column grids, while narrower viewports progressively reorganise them into fewer columns and additional rows. Paired cards stack vertically, and larger groups of options adjust to the available width, maintaining readable labels, comfortable spacing and accessible selection areas without horizontal scrolling.

The overall experience is designed as an intuitive journey, moving from creative inspiration and personal preferences towards the practical details of placing an order. A Back to Top button provides convenient navigation through the longer form, while unauthenticated visitors receive a login prompt when attempting to interact with it. The final action leads to the order details stage, separating the creative decision-making process from the subsequent checkout and payment steps.


### Where to Buy Page

The Where to Buy page redesigns an existing section of Frank Moth's website, transforming a scattered collection of external retailer links into a structured and informative shopping guide. The main objective is to improve product discoverability and help visitors identify where to purchase the types of products they are interested in.

The layout uses a simple two-column grid of horizontal retailer cards, with Frank Moth's official Etsy shop given greater prominence through a separate highlighted link at the top. Each retailer is presented with a clearly identifiable name, an external link and a brief description of the products available, supported by subtle hover effects that communicate interactivity. The restrained visual design keeps the focus on the information and makes the available purchasing options easy to scan.

The most significant improvement is the addition of product descriptions beneath each retailer. Previously, visitors were presented with largely unstructured links and had to open individual retailer websites to discover what they offered. This made comparing options time-consuming and obscured the variety of products featuring Frank Moth's artwork, beyond traditional prints and canvases. The redesigned page introduces visitors to additional possibilities, including clothing, home décor, phone cases and other merchandise, without requiring them to investigate numerous external websites.

By presenting this information together, the page reduces unnecessary navigation, supports informed purchasing decisions and makes the range of available products more visible. This improves the overall shopping experience while creating more opportunities for visitors to discover products and potentially generate sales for the artists.

The responsive layout adapts the two-column grid to a single column on smaller screens, preserving the clarity of the retailer descriptions and keeping external links easy to access on mobile devices.


#### Customer Details, Checkout and Confirmation Pages

The commission process continues through the Customer Details and Checkout stages, followed by an Order Confirmation page. Unlike the more expressive Commissions page, these pages deliberately use a minimal design with clean white backgrounds, allowing visitors to focus on entering their personal information, completing payment and reviewing their order confirmation. Forms, buttons and typography are styled consistently with the website's visual identity, maintaining a cohesive experience throughout the process. This restrained approach reduces visual distractions during the more practical stages of ordering, while the confirmation page provides a clear conclusion to the commission journey.


### Login, Logout and Signup Pages

The Login, Sign Up and Logout pages use Django's existing authentication functionality, with their forms and interface elements customised to match the website's colour palette, typography and overall visual identity. Rather than presenting these necessary interactions as purely functional pages, the design uses them as another opportunity to showcase Frank Moth's artwork and create a more engaging user experience.

Three distinct background collages were created specifically for these pages, each featuring eight artworks from the same collection. The colourful compositions provide visual interest and introduce visitors to additional examples of the artists' work, encouraging further exploration of the portfolio. The authentication forms are presented in clean, centrally positioned white panels, creating a clear contrast with the expressive backgrounds and keeping the forms readable and easy to use.

The layouts are responsive, with the forms adapting to smaller screens while the background collages remain positioned at the top. As the viewport narrows, a smaller portion of each collage becomes visible, preserving the colourful atmosphere without compromising the usability of the authentication forms. This approach maintains visual consistency across the website while turning routine account interactions into a more memorable part of the visitor experience.


### Contact Page

The Contact page follows a simple, functional design, with a clearly structured contact form styled to match the website's colour palette, typography and visual identity. On larger screens (992px and above), the layout uses two columns, positioning the form on the left and Frank Moth's monogram on the right. Below this breakpoint, the monogram is hidden and the form occupies the available width, maintaining a clear and accessible experience. The restrained design keeps attention on the primary purpose of the page: allowing visitors to contact the artists easily, without unnecessary visual distractions.


### My Account Page

The My Account page is available to authenticated users and brings together two new features: My Favourites and My Commissions. Both aim to encourage continued engagement with the website by allowing visitors to save artworks they are interested in and revisit their previous commission orders.

The My Favourites feature addresses an important limitation of Frank Moth's previous website, where visitors could browse artworks but had no way to save or compare their preferred pieces. This was particularly relevant when considering larger artworks, framed prints or installations for residential and commercial interiors, where purchasing decisions often require time, comparison and discussion with family members or interior designers. Inspired by firsthand experience of this difficulty, the feature was introduced to support a more considered purchasing journey, allowing users to gradually build and revisit a personal shortlist rather than repeatedly searching through the entire portfolio.

Authenticated users can add or remove artworks from their favourites through the Artwork Detail page. A confirmation message provides immediate feedback when an artwork is saved, including a direct link to My Favourites. Within My Account, saved artworks are displayed in a responsive image gallery, using four columns on larger screens, three on medium screens and two on mobile devices. Subtle hover effects, including a slight movement and shadow, provide visual feedback without distracting from the artwork. Each image links back to its Artwork Detail page, where users can review the piece or remove it from their favourites. The navigation also adapts to the user's journey: when arriving from My Favourites, the usual Back to Collection link becomes Back to My Favourites, providing a more intuitive return path.

The second section, My Commissions, provides users with a permanent record of their bespoke artwork orders. Commissions are presented in a simple, structured table with expandable rows, allowing users to reveal the details of individual orders without overwhelming the page with information. This keeps the account area organised and makes previous commission information easy to access whenever needed.

Together, these features extend the website beyond a portfolio for browsing artwork, supporting both the decision-making process before a purchase and access to order information afterwards.


## Artist Dashboard

The Artist Dashboard was developed as a dedicated management interface, allowing Frank Moth to maintain their artwork catalogue independently. Unlike the public-facing pages, which prioritise visual presentation and visitor engagement, the dashboard focuses on efficiency, clarity and practical administration. Its design follows the website's established visual identity while introducing a more compact, information-oriented layout suited to everyday catalogue management.

The website's main navigation remains visible throughout the dashboard, with an additional Dashboard link appearing for authenticated artist accounts. Within the dashboard, a dedicated navigation menu provides access to its four main sections: Artworks, Collections, Commissions and Messages. The currently selected section is visually highlighted, helping artists maintain their orientation and move efficiently between management tasks. On wider screens, this menu appears as a sidebar alongside the content, while on narrower screens it moves above the main dashboard area.

### Manage Artworks Page

The Manage Artworks Page serves as the dashboard's main landing page, providing a visual overview of the complete artwork catalogue alongside tools for searching, filtering and maintaining individual records.

Artworks are presented in a responsive grid of compact cards, displaying six columns on extra-large screens, four below 1400px, three below 1200px and two below 768px, including mobile devices. Each card includes an artwork thumbnail, title, description and clearly identified actions to view, edit or delete the corresponding record. A prominent Add Artwork link provides access to creating new entries.

Pagination was deliberately set to 36 artworks per page, allowing the artists to scan a substantial portion of their catalogue visually without frequent page changes. Unlike the public gallery, where larger images encourage appreciation of individual works, the dashboard uses smaller thumbnails because their primary purpose is identification. This creates a more efficient overview for artists already familiar with their work.

Search, filtering and sorting controls are positioned above the grid, allowing artworks to be located by title, collection or metadata completeness, including the presence or absence of a year, description or Etsy URL. Sorting options include alphabetical order, artwork year and most recently added. These controls can be combined to support different catalogue management tasks.

The filtering system was informed by firsthand experience of organising and maintaining the artwork database during development. Since only an artwork's title and image are required when creating a record, additional information can be completed or updated later. For example, artists may need to identify works without descriptions, add missing dates or connect Etsy listings as products become available for purchase. The dashboard therefore supports ongoing catalogue maintenance rather than treating artwork management as a simple process of adding and deleting records.


#### Artwork Overview Page

The Artwork Overview page provides a more comprehensive view of an individual artwork, accessed through the eye icon on its dashboard card. A larger image is displayed on the left, with the artwork's information organised on the right. Any missing details are clearly marked as "Not provided", helping artists quickly identify information that may need updating. Edit and Delete actions are available directly from this page, while a Back to Artworks link provides easy navigation to the main artwork overview.


#### Add / Edit Artwork Pages

The Add and Edit Artwork pages share the same simple, clearly structured form. Artists can upload an image, enter a title and description, and assign the artwork to an existing collection. The Edit Artwork page can be accessed through the pencil icon on an artwork's dashboard card or through the corresponding link on its individual artwork page. When editing, the form is pre-filled with the existing information, allowing artists to update individual details without re-entering everything. The minimal layout prioritises clarity and ease of use, while a Back to Artworks link provides convenient navigation to the main artwork overview.


#### Delete Artwork Page

The Delete Artwork page provides a straightforward confirmation step to prevent accidental removal of artwork records. Accessible through the delete icon on the Artworks List or the corresponding action on the Artwork Details page, it displays the artwork's image and title so the artist can clearly identify the selected record. A confirmation message asks whether they wish to proceed, with clearly distinguished Delete and Cancel options. A Back to Artworks link also provides a convenient return to the main catalogue.


### Manage Collections Page

The Manage Collections page provides a clear, structured overview of the artwork collections, displayed as a vertical list with one row per collection. Each row includes a square thumbnail of the collection's cover image, its title, the number of artworks it contains and its current display order on the public-facing website.

An important addition is the ability for artists to **control the order in which collections appear on the public Art page**. Using simple up and down arrows, they can rearrange collections directly from the dashboard, giving them greater creative control over how their portfolio is presented and which collections receive prominence. This functionality allows the artists to adjust the presentation of their work as their catalogue evolves, without requiring developer intervention.

Each collection title links to its individual management page, while Edit and Delete buttons provide direct access to the corresponding actions. An Add Collection button at the top allows new collections to be created easily. The compact, list-based layout prioritises clarity and efficient management, bringing the essential collection management tools together in one place.

#### Collection Overview Page

The Collection Overview page provides a detailed view of an individual collection, following the same clear layout as the Artwork Details page. A larger image of the collection's cover is displayed alongside its title, description and total number of artworks. Edit and Delete actions are available directly from this page, allowing artists to manage the collection without returning to the main list. A Back to Collections link at the top provides convenient navigation to the Manage Collections page.

#### Add / Edit Collection Pages

The Add and Edit Collection pages share a simple, clearly structured form for entering a collection's name and description. When creating a new collection, the fields are empty, while editing an existing collection presents its information pre-filled for convenient updates.

An important additional feature allows artists to **select and change the collection's cover artwork directly through the dashboard**. The Edit Collection form presents a grid of eight artwork thumbnails, with a Show All option to reveal the remaining artworks. The currently selected cover is clearly identified by a green border and checkmark, providing immediate visual feedback. Artists can choose a different cover simply by selecting another image.

This functionality gives the artists greater creative control over the presentation of their collections on the public website. They can refresh the appearance of the Art page, highlight different artworks and adapt their portfolio presentation over time without requiring developer intervention.

#### Delete Collection Page

The Delete Collection page is accessed through the Delete button on the Manage Collections page and provides a dedicated confirmation step to prevent accidental removal of collections.

An additional safeguard protects collections that still contain artworks. If a collection is not empty, deletion is blocked and a clear explanation informs the artist that its artworks must first be reassigned to other collections. In this case, no Delete button is presented, preventing the accidental loss of associated artwork records. Instead, navigation links allow the artist to return either to the individual Collection Overview page or to the Manage Collections list.

This approach prioritises the integrity of the artwork catalogue while providing clear guidance on the steps required before a collection can be safely deleted.


### Commissions & Messages Pages

The Manage Commissions and Manage Messages pages follow a similar, minimal design, prioritising clarity and efficient access to information. Both present records in structured lists with expandable rows, allowing artists to review individual commissions or messages without navigating away from the page.

The Manage Commissions page includes filtering options to distinguish between pending and completed orders. Artists can expand a commission to review its details and mark it as completed when the work has been fulfilled. This status is intended exclusively for internal organisation and does not communicate progress updates to customers.

Although the artists receive email notifications for both new commissions and contact messages, these dashboard sections provide a permanent, centralised archive that can be consulted independently of their email inbox. This supports better organisation, makes previous information easier to retrieve and provides a practical overview of incoming requests and commissioned work.