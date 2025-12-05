<!--
Sync Impact Report:
- Version change: Template → 1.0.0
- Added principles:
  1. Spec-Driven Writing
  2. Technical Accuracy
  3. Beginner-Friendly Style
  4. Reproducibility
  5. AI-Native Modularity
- Added sections:
  - Key Standards
  - Constraints
  - Success Criteria
- Removed sections: None (PRINCIPLE_6 removed from template as unused)
- Templates requiring updates:
  ✅ spec-template.md - Aligned with spec-driven approach
  ✅ plan-template.md - Constitution Check section will reference these principles
  ✅ tasks-template.md - Task structure supports reproducibility principle
  ⚠ README.md - Does not exist, should be created with project overview
- Follow-up TODOs: Create README.md with project description and setup instructions
-->

# Docusaurus Technical Book Constitution

## Core Principles

### I. Spec-Driven Writing

No content without a spec. All documentation must be preceded by a specification that
defines scope, audience, and acceptance criteria. Every chapter, tutorial, or code
example MUST have a corresponding spec file in the `/specs/` directory before writing
begins. This ensures clarity of intent and enables validation against requirements.

**Rationale**: Prevents scope creep, maintains consistency, and enables systematic
validation of all content against defined requirements.

### II. Technical Accuracy

All technical content MUST be based on official documentation from authoritative
sources. Claims about tools, commands, APIs, or workflows MUST be verified against
the official documentation of Docusaurus, GitHub, and related technologies. When
official docs are ambiguous or incomplete, this MUST be noted explicitly with
references using APA citation format.

**Rationale**: Ensures readers can trust the content and trace information back to
authoritative sources, reducing confusion and errors.

### III. Beginner-Friendly Style

Content MUST be written in clear, beginner-friendly instructional style. Assume
readers are new to the topic. Avoid jargon without explanation. Use concrete
examples, step-by-step instructions, and plain language. Every command MUST be
explained before use. Every concept MUST be introduced before application.

**Rationale**: Maximizes accessibility and learning effectiveness for the target
audience of technical beginners.

### IV. Reproducibility

All tutorials, commands, and workflows MUST be reproducible. Readers following the
exact steps MUST achieve the same results. This requires:
- Explicit version specifications for all tools and dependencies
- Complete command sequences with no assumed prior setup
- Clear prerequisite states before each procedure
- Validation steps to confirm successful completion

**Rationale**: Enables readers to learn by doing and validates content correctness
through executable verification.

### V. AI-Native Modularity

Content MUST be structured in modular, reusable units suitable for iterative
improvement by AI agents and human editors. Each module (chapter, section, tutorial)
MUST:
- Have clear boundaries and dependencies
- Be independently updateable without breaking other modules
- Include metadata for version tracking and change history
- Follow consistent structural patterns for automated processing

**Rationale**: Facilitates continuous improvement, enables AI-assisted authoring and
maintenance, and supports systematic content evolution.

## Key Standards

### Formatting Consistency

All content MUST use consistent formatting conventions:
- Commands: Display in fenced code blocks with language identifiers
- File paths: Use monospace inline code formatting
- File trees: Use text-based tree diagrams with consistent indentation
- Procedure steps: Use numbered lists with one action per item
- Code examples: Include language tag, filename comment, and syntax highlighting

### Validation Discipline

All instructional content MUST be validated through execution:
- Build instructions MUST be tested from a clean environment
- Commands MUST be run and outputs captured
- Deployment procedures MUST be executed end-to-end
- Screenshots MUST reflect actual tool states, not mockups

### External References

When referencing external information:
- Use APA citation format for all external sources
- Include access dates for web resources
- Link to specific versions or commit hashes when available
- Maintain a centralized bibliography/references section

### Version Control Workflow

All changes MUST follow disciplined version control practices:
- Meaningful commit messages following conventional commit format
- One logical change per commit
- Branch naming aligned with spec file naming
- PR descriptions referencing the spec that justifies the change

## Constraints

### Output Format

Content MUST be authored in Markdown format compatible with Docusaurus v3+. No
proprietary formats, binary documents, or custom markup extensions are permitted.
All content files MUST have `.md` or `.mdx` extension and conform to Docusaurus
front matter requirements.

### Deployment Target

The book MUST deploy to GitHub Pages via GitHub Actions. Deployment configuration
MUST be automated, reproducible, and documented. Manual deployment steps are not
permitted in production workflow. All deployment requirements (build commands,
environment variables, secrets) MUST be documented in the spec.

### Specification Storage

All specifications MUST be stored in the `/specs/` directory following the Spec-Kit
Plus structure and naming conventions. Specs MUST NOT be embedded in content files
or maintained separately from the repository. The source of truth for all
requirements is the spec file, not inline comments or external documents.

### Technology Version

Docusaurus version 3 or higher MUST be used. No legacy Docusaurus v1 or v2 features
are permitted. Dependency versions MUST be explicitly locked in `package.json` or
equivalent. Upgrades MUST follow a documented migration plan with validation steps.

## Success Criteria

The project meets its constitutional requirements when:

### Build Success

The book builds successfully without errors or warnings. The build process completes
in a clean environment following only the documented setup instructions. All
dependencies resolve correctly and all content renders as intended.

### Spec Compliance

All content aligns with and can be traced back to declared specifications. Every
chapter, tutorial, and code example has a corresponding spec file. No content exists
that lacks specification justification.

### Reproducibility Verification

A beginner user following the instructions from a clean starting state can
successfully build, develop, and deploy the book. Validation includes:
- Setup from zero to working environment
- Content authoring workflow
- Build and preview locally
- Deploy to GitHub Pages

### Content Quality Standards

All content demonstrates:
- Technical accuracy verified against official documentation
- Clear, beginner-friendly writing style
- Proper formatting using established standards
- Appropriate citations for external references
- AI-native modular structure for maintainability

## Governance

### Amendment Procedure

Amendments to this constitution require:
1. Documented rationale explaining the need for change
2. Impact analysis on existing content and workflows
3. Migration plan for bringing existing content into compliance
4. Approval from project maintainers
5. Version increment following semantic versioning

### Versioning Policy

Constitution versions follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Backward-incompatible changes to core principles or removal of
  requirements
- **MINOR**: Addition of new principles, standards, or constraints that expand scope
- **PATCH**: Clarifications, wording improvements, or non-semantic refinements

### Compliance Review

All content contributions MUST be reviewed for constitutional compliance before
merge. Reviewers MUST verify:
- Corresponding spec exists and justifies the content
- Formatting standards are followed
- Technical claims are accurate and cited
- Instructions are reproducible
- Modular structure is maintained

### Complexity Justification

Any violation of constitutional principles MUST be explicitly justified and
documented. Complexity that conflicts with these principles requires:
- Clear statement of which principle is violated
- Explanation of why the violation is necessary
- Description of alternatives considered and rejected
- Approval from project maintainers

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
