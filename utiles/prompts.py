typst_content = """

// ===============================
// Imports
// ===============================
#import "@preview/brilliant-cv:2.0.6": letter

// ===============================
// Metadata (merged from metadata.toml, English only)
// ===============================
#let metadata = (
  language: "en",

  layout: (
    awesome_color: "skyblue",
    before_section_skip: "1pt",
    before_entry_skip: "1pt",
    before_entry_description_skip: "1pt",
    paper_size: "a4",

    fonts: (
      regular_fonts: ("Source Sans Pro", "Source Sans 3"),
      header_font: "Roboto",
    ),

    header: (
      header_align: "left",
      display_profile_photo: true,
      profile_photo_radius: "50%",
      info_font_size: "10pt",
    ),

    entry: (
      display_entry_society_first: true,
      display_logo: true,
    ),
  ),

  personal: (
    first_name: "Silin",
    last_name: "Zhao",

    info: (
      github: "scofild429",
      phone: "01605031334",
      email: "silin110zhao@gmail.com",
      linkedin: "silin-zhao",
      homepage: "silinzhao.com",
      extraInfo: "German (C1) | English (C1) | Emacser",
    ),
  ),

  lang: (
    en: (
      header_quote: "Experienced AI developer in HPC",
      cv_footer: "Curriculum vitae",
      letter_footer: "Cover letter",
    ),
  ),
)

// ===============================
// Letter layout
// ===============================
#show: letter.with(
  metadata,
  myAddress: "Süderquerweg 286, 21037 Hamburg",
  recipientName: "Company Name Here",
  recipientAddress: "Company Address Here",
  date: datetime.today().display(),
  subject: "Application for the position of Y in X",
)

// ===============================
// Letter content
// ===============================
Dear Hiring Group of X,

I am writing to apply for the Y position at X.

I am particularly interested in this role because it aligns strongly with my background in AI development, high-performance computing, and applied machine learning. Through my academic and professional experience....
...
I would welcome the opportunity to further discuss how my skills and motivation could contribute to your team.

Sincerely,  

the name of application
"""


tone_setting = """
 Change the content to meet the requirements of the job description.
You have a schema as a guide.

- 1. Understand the job description: Mark keywords and break down the requirements:

  + Must-have criteria (without which one is chanceless → definitely highlight).

  + Nice-to-have criteria (only mention if you actually have them).

- 2. Selection of relevant content
  + Relevant = Everything directly stated in the job description. Irrelevant = Everything not mentioned and without a direct connection to the job. 👉 Rule: Only describe relevant content in detail. At most, briefly mention or completely omit irrelevant content.

- 3. Structure of the cover letter
  + Introduction:
     Why this specific position and institution? (1–2 sentences), incorporate keywords from the job description.
  + Professional Strengths (Must-have criteria):
     Name 2–3 main requirements of the position and back up your own experience with a concrete example. Write actively: “I have optimized … developed … supported …“
  + Teamwork & Communication:
     Through my work and activities during my studies, I have gained good experience in these areas. You can rephrase this to make my description more convincing.

- 4. Motivation / Conclusion
  + Contribution to this research field, invitation for an interview.


+ Instructions for the adaptation:
- Short sentences, not too technical. Do not write project reports → only what convinces the employer.
- Emphasize my qualifications and experiences that directly match the job requirements (e.g., specific skills, industry knowledge, or successes).
- Remove or adapt parts that are not relevant and add new, fitting elements based on my original text.
- Maintain the structure: Introduction (reference to the position), Main Body (qualifications and motivation), Conclusion (call to interview).
- Ensure the text is professional, error-free, concise, and limited to a maximum of one A4 page (approx. 300-500 words).
- Use formal english language, suitable for an application in Germany/Austria/Switzerland.
- At the end, provide a brief explanation of the changes you made and why.

+ Checklist before sending:
- Does my text include all must-have criteria from the job description?
- Have I removed or significantly shortened irrelevant skills?
- Is it clear why I want to work there specifically?
- Is my tone appropriate: professional, focused, motivated?

"""
