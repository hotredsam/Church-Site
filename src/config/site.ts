export type NavItem = {
  label: string;
  href: string;
  children?: { label: string; href: string }[];
};

export const nav: NavItem[] = [
  {
    label: "Home",
    href: "/"
  },
  {
    label: "About",
    href: "/about",
    children: [
      { label: "Plan Your Visit", href: "/about/plan-your-visit" },
      { label: "Staff & Leadership", href: "/about/staff-leadership" },
      { label: "What We Believe", href: "/about/what-we-believe" },
      { label: "Our Story", href: "/about/our-story" }
    ]
  },
  {
    label: "Get Connected",
    href: "/get-connected",
    children: [
      { label: "Contact / Connect Card", href: "/get-connected/contact-connect-card" },
      { label: "K-Groups", href: "/get-connected/k-groups" },
      { label: "Car Maintenance Help", href: "/get-connected/car-maintenance-help" },
      { label: "Kaleo Kids", href: "/get-connected/kaleo-kids" },
      { label: "Kaleo Student Ministry", href: "/get-connected/kaleo-student-ministry" },
      { label: "Men's Ministry", href: "/get-connected/mens-ministry" },
      { label: "Church Center App", href: "/get-connected/church-center-app" }
    ]
  },
  {
    label: "Grow",
    href: "/grow",
    children: [
      { label: "Sermons", href: "/grow/sermons" },
      { label: "Bible Reading Plan", href: "/grow/bible-reading-plan" },
      { label: "Prayer", href: "/grow/prayer" },
      { label: "Baptism", href: "/grow/baptism" },
      { label: "Membership", href: "/grow/membership" },
      { label: "Serve", href: "/grow/serve" },
      { label: "Re|Engage", href: "/grow/re-engage" }
    ]
  },
  {
    label: "Events",
    href: "/events",
    children: [
      { label: "Calendar", href: "/events/calendar" }
    ]
  },
  {
    label: "Give",
    href: "/give"
  }
];

export const footerLinks = {
  quick: [
    { label: "Live Stream", href: "/live-stream" },
    { label: "Advent Resources", href: "/advent-resources" },
    { label: "Contact", href: "/get-connected/contact-connect-card" },
    { label: "Team Portal", href: "/team-portal" }
  ],
  external: [
    { label: "Church Center", href: "https://kaleoalaska.churchcenter.com" },
    { label: "Give", href: "https://kaleoalaska.churchcenter.com/giving" },
    { label: "Connect Card", href: "https://kaleoalaska.churchcenter.com/people/forms/492204" },
    { label: "Live Stream", href: "https://www.youtube.com/@kaleochurch907" }
  ]
};

export const canonical = {
  org: "https://www.kaleoalaska.org",
  churchCenter: "https://kaleoalaska.churchcenter.com",
  connectCard: "https://kaleoalaska.churchcenter.com/people/forms/492204",
  giving: "https://kaleoalaska.churchcenter.com/giving",
  baptism: "https://kaleoalaska.churchcenter.com/people/forms/629175",
  prayer: "https://kaleoalaska.churchcenter.com/people/forms/573723",
  events: "https://kaleoalaska.churchcenter.com/calendar",
  watch: "https://www.youtube.com/@kaleochurch907",
  listen: "https://open.spotify.com/show/0nQ52GXMcHC4JgAoecfTr2"
};

export const siteMeta = {
  title: "Kaleo Church",
  description: "Kaleo Church in Anchorage, Alaska. Following Jesus together.",
  email: "info@kaleoalaska.org",
  phone: "(907) 555-0123",
  address: "Anchorage, AK"
};

export const documents = {
  adventGuide: "https://storage.snappages.site/KQ4M3M/assets/files/Kaleo-Advent-Guide-2024.pdf",
  adventReadings: "https://storage.snappages.site/KQ4M3M/assets/files/The-Incarnation-Advent-Readings.pdf",
  smallGroupPolicies: "https://storage.snappages.site/KQ4M3M/assets/files/SMALL-GROUP-POLICIES.pdf",
  membershipCovenant: "https://storage.snappages.site/KQ4M3M/assets/files/Covenant-Membership-Kaleo.pdf",
  jobDescriptions: {
    kaleoKidsDirector: "https://cpmfiles1.com/kaleoalaska.org/JD-KALEO-KIDS-DIRECTOR-2020.pdf",
    operationsDirector: "https://cpmfiles1.com/kaleoalaska.org/operationsdirector-job-description-2024.pdf",
    churchMultiplicationResident: "https://cpmfiles1.com/kaleoalaska.org/churchmultiplicationresident-jobdescription-2024.pdf",
    worshipLeader: "https://cpmfiles1.com/kaleoalaska.org/worshipleader-job-description-2024.pdf",
    womenDirector: "https://cpmfiles1.com/kaleoalaska.org/womendirector-job-description-2024.pdf",
    youthDirector: "https://cpmfiles1.com/kaleoalaska.org/youthdirector-job-description-2024.pdf",
    communicationDirector: "https://cpmfiles1.com/kaleoalaska.org/communicationdirector-job-description-2024.pdf"
  }
};

export const legacyToNew = [
  ["/", "/"],
  ["/about", "/about"],
  ["/about/plan-your-visit", "/about/plan-your-visit"],
  ["/about/staff-and-leadership", "/about/staff-leadership"],
  ["/about/what-we-believe", "/about/what-we-believe"],
  ["/about/our-story", "/about/our-story"],
  ["/josh-sawyer", "/about/staff/josh-sawyer"],
  ["/tyler-dumbrille", "/about/staff/tyler-dumbrille"],
  ["/get-connected", "/get-connected"],
  ["/get-connected/connect-card", "/get-connected/contact-connect-card"],
  ["/get-connected/small-groups", "/get-connected/k-groups"],
  ["/get-connected/kaleo-kids", "/get-connected/kaleo-kids"],
  ["/get-connected/kaleo-student-ministry", "/get-connected/kaleo-student-ministry"],
  ["/get-connected/mens-ministry-resources", "/get-connected/mens-ministry"],
  ["/get-connected/church-center-app", "/get-connected/church-center-app"],
  ["/grow", "/grow"],
  ["/grow/sermons", "/grow/sermons"],
  ["/grow/bible-reading-plan", "/grow/bible-reading-plan"],
  ["/grow/prayer", "/grow/prayer"],
  ["/grow/baptism", "/grow/baptism"],
  ["/grow/membership", "/grow/membership"],
  ["/grow/serve", "/grow/serve"],
  ["/grow/reengage", "/grow/re-engage"],
  ["/upcoming-events", "/events"],
  ["/give", "/give"],
  ["/live-stream", "/live-stream"],
  ["/advent-resources", "/advent-resources"],
  ["/jd-kaleo-kids-director", "/jobs/jd-kaleo-kids-director"],
  ["/jd-operations-director", "/jobs/jd-operations-director"],
  ["/jd-church-multiplication-resident", "/jobs/jd-church-multiplication-resident"],
  ["/jd-worship-leader", "/jobs/jd-worship-leader"],
  ["/jd-women-director", "/jobs/jd-women-director"],
  ["/jd-youth-director", "/jobs/jd-youth-director"],
  ["/jd-communication-director", "/jobs/jd-communication-director"]
] as const;
