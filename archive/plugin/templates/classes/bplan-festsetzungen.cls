% bplan-festsetzungen.cls
% Universal document class for German B-Plan Textliche Festsetzungen
% (Teil B Text der Satzung). Encapsulates the structural domain
% (article-based, infinite-page geometry, German language, sans-serif
% body convention, enumerate styling for hierarchical Festsetzungs-
% Regeln, helpers for Verfahrensvermerk tabbing blocks).
%
% NOT included: page margins beyond the infinite-page envelope, font
% family beyond sans-default, header layout, color theme, office
% identity. Those are office-specific and live in office-style.sty.
%
% Usage:
%   \documentclass{bplan-festsetzungen}
%   \usepackage{office-style}
%   \input{office-identity}
%   \input{Projektdaten}
%   \begin{document}
%   ...
%   \end{document}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bplan-festsetzungen}[2026/04/28 v0.1 B-Plan Festsetzungen]

% ---- Pass options through to article --------------------------------
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\LoadClass[12pt]{article}

% ---- Encoding & language --------------------------------------------
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[ngerman]{babel}

% ---- Typographic baseline -------------------------------------------
\RequirePackage[final]{microtype}

% ---- Sans-serif body (convention for "binding rules" portion) -------
% Office may override the specific sans family in office-style.sty;
% the sans-default itself is universal for Festsetzungen.
\renewcommand{\familydefault}{\sfdefault}

% ---- Hyphenation tuning ---------------------------------------------
\setlength{\emergencystretch}{3em}

% ---- Geometry — single infinite page --------------------------------
% A4 width, paperheight maxed (~141 cm; TeX limit ~575 cm). No
% margins inside the geometry — content controls its own indentation.
% Will not paginate; output is one PDF page designed to be embedded
% as Teil B Text of the B-Plan Satzung document.
\RequirePackage{geometry}
\geometry{
  paperwidth=210mm,
  paperheight=4000pt,
  left=0in, right=0in,
  top=0in, bottom=0in
}

% ---- Section title formatting (universal default: compact) ----------
% Office may override in office-style.sty for different sizing.
\RequirePackage{titlesec}
\titleformat{\section}
  {\normalfont\normalsize\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries}{\thesubsubsection}{1em}{}

% ---- enumerate styling helpers --------------------------------------
\RequirePackage{enumitem}
\RequirePackage{url}

% ---- Verfahrensvermerk tabbing helper -------------------------------
% Standard 3-column signature block: location/date | Siegel | name.
% Office may override widths in office-style.sty.
\providecommand{\VerfahrensvermerkSignatur}[3]{%
  \begin{tabbing}
    \hspace{6cm} \= \hspace{4cm} \= \kill
    #1, \> Siegel \> \hspace{8pt} #2 \\
    \> \> --- #3 ---
  \end{tabbing}%
}

% ---- Project metadata framework (defaults) --------------------------
% Mirror of bplan-begruendung.cls. Projektdaten.tex MUST override
% every one with concrete values.
\providecommand{\Gemeinde}{---GEMEINDE---}
\providecommand{\Stadt}{---STADT---}
\providecommand{\Gemarkung}{---GEMARKUNG---}
\providecommand{\Ortsteil}{---ORTSTEIL---}
\providecommand{\Landkreis}{---LANDKREIS---}
\providecommand{\Bundesland}{---BUNDESLAND---}
\providecommand{\BPlanAbrv}{B-Plan}
\providecommand{\BPlanNr}{---N---}
\providecommand{\BPlanName}{---BPLAN-NAME---}
\providecommand{\BPlan}{---BPLAN-PROSE-LOWERCASE---}
\providecommand{\BPlanTyp}{---BPLAN-PROSE-CAPITALIZED---}
\providecommand{\GeltungsbereichHa}{---HA---}
\providecommand{\GeltungsbereichHaSolar}{---HA---}
\providecommand{\Planungsregion}{---PLANUNGSREGION---}

% ---- Office identity macro defaults ---------------------------------
\providecommand{\OfficeName}{---OFFICE-NAME---}
\providecommand{\OfficeShort}{---OFFICE-SHORT---}
\providecommand{\OfficeAddressLines}{---OFFICE-ADDRESS---}
\providecommand{\OfficePhone}{}
\providecommand{\OfficeEmail}{}
\providecommand{\OfficeWeb}{}
\providecommand{\OfficeSignatureBlock}{---OFFICE-SIGNATURE---}
\providecommand{\OfficeSigner}{---OFFICE-SIGNER---}

\endinput
