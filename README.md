# Docusaurus Technical Book

A technical book built with **Docusaurus v3**, **Spec-Kit Plus**, and **Claude Code**, demonstrating spec-driven development and automated deployment to GitHub Pages.

## Project Overview

This project creates a technical book that follows rigorous standards for:

- **Spec-driven writing** - No content without specifications
- **Technical accuracy** - All content based on official documentation
- **Beginner-friendly style** - Clear, accessible instruction
- **Reproducibility** - All tutorials and commands are verified
- **AI-native modularity** - Structured for continuous improvement

## Quick Start

### Prerequisites

- **Node.js** 18.0 or higher
- **npm** (comes with Node.js)
- **Git** for version control

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai_humanoid_robotics_as.git
cd ai_humanoid_robotics_as

# Install dependencies
npm install

# Start development server
npm start
```

The site will open at `http://localhost:3000`.

### Build for Production

```bash
# Build static files
npm run build

# Serve production build locally
npm run serve
```

The production build will be in the `build/` directory.

## Project Structure

```
ai_humanoid_robotics_as/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment workflow
├── .specify/
│   ├── memory/
│   │   └── constitution.md     # Project constitution (principles & standards)
│   └── templates/              # Spec-Kit Plus templates
├── blog/                       # Blog posts
│   ├── authors.yml
│   └── 2025-12-05-welcome.md
├── docs/                       # Documentation pages
│   ├── intro.md
│   └── tutorial-basics/
│       └── tutorial-intro.md
├── history/
│   └── prompts/                # Prompt History Records (PHRs)
│       └── constitution/
├── specs/                      # Feature specifications
│   └── 001-initial-setup/
│       └── spec.md
├── src/
│   ├── components/             # React components
│   ├── css/
│   │   └── custom.css          # Custom styles
│   └── pages/
│       ├── index.tsx           # Homepage
│       └── index.module.css
├── static/
│   └── img/                    # Static images
│       └── logo.svg
├── docusaurus.config.ts        # Docusaurus configuration
├── sidebars.ts                 # Sidebar configuration
├── package.json                # Dependencies (locked versions)
├── tsconfig.json               # TypeScript configuration
└── README.md                   # This file
```

## Development Workflow

### Creating New Content

1. **Write a specification** in `specs/<feature-name>/spec.md` following the spec template
2. **Implement content** based on the spec
3. **Validate** that content matches spec requirements
4. **Commit** with meaningful commit message

### NPM Scripts

- `npm start` - Start development server with hot reload
- `npm run build` - Build production static files
- `npm run serve` - Serve production build locally
- `npm run clear` - Clear Docusaurus cache
- `npm run deploy` - Deploy to GitHub Pages (manual)

## Deployment

### Automated Deployment (Recommended)

The project uses GitHub Actions for automated deployment:

1. Push code to `main` or `master` branch
2. GitHub Actions automatically builds the site
3. Site deploys to GitHub Pages at `https://YOUR_USERNAME.github.io/ai_humanoid_robotics_as/`

**Note**: Ensure GitHub Pages is enabled in repository settings and set to deploy from GitHub Actions.

### Manual Deployment

```bash
# Build the site
npm run build

# Deploy (requires GitHub authentication)
GIT_USER=YOUR_USERNAME npm run deploy
```

## Configuration

### Update GitHub Username

Before deploying, update these files with your GitHub username:

**`docusaurus.config.ts`** (line 8):
```typescript
const githubUsername = 'YOUR_USERNAME'; // Change this
```

**`blog/authors.yml`**:
```yaml
admin:
  url: https://github.com/YOUR_USERNAME  # Change this
  image_url: https://github.com/YOUR_USERNAME.png  # Change this
```

### Docusaurus Configuration

Main configuration is in `docusaurus.config.ts`:

- **Title & tagline**: Update site metadata
- **URL & baseUrl**: Configure for GitHub Pages
- **Theme**: Customize colors, navbar, footer
- **Plugins**: Add additional Docusaurus plugins

## Constitution & Principles

This project follows the principles defined in `.specify/memory/constitution.md`:

### Core Principles

1. **Spec-Driven Writing** - All content must have corresponding specifications
2. **Technical Accuracy** - Content based on official documentation with APA citations
3. **Beginner-Friendly Style** - Clear, accessible, step-by-step instruction
4. **Reproducibility** - All commands and workflows must be executable
5. **AI-Native Modularity** - Structured for iterative AI/human improvement

### Standards

- **Formatting Consistency** - Commands in code blocks, consistent file trees
- **Validation Discipline** - All instructions tested from clean environment
- **External References** - APA citation format for all external sources
- **Version Control** - Conventional commit messages, meaningful PRs

### Constraints

- **Output Format**: Markdown (Docusaurus v3+) only
- **Deployment**: GitHub Pages via GitHub Actions (automated)
- **Specs**: Stored in `/specs/` directory
- **Technology**: Docusaurus v3+ required

## Troubleshooting

### Port Already in Use

If `npm start` fails with "Port 3000 already in use":

```bash
# Use different port
npm start -- --port 3001
```

### Build Fails

```bash
# Clear cache and rebuild
npm run clear
npm run build
```

### Dependencies Issues

```bash
# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Contributing

1. Create a feature specification in `specs/<feature-name>/spec.md`
2. Create a feature branch following naming convention
3. Implement content following the spec
4. Ensure build succeeds: `npm run build`
5. Commit with conventional commit format
6. Create pull request referencing the spec

## Resources

- **Docusaurus Documentation**: https://docusaurus.io/docs
- **Spec-Kit Plus**: Templates in `.specify/templates/`
- **Constitution**: `.specify/memory/constitution.md`
- **Specifications**: `specs/` directory

## License

This project is licensed under the MIT License.

## Support

For issues or questions:

- Check the [Docusaurus documentation](https://docusaurus.io/docs)
- Review existing specifications in `specs/`
- Open an issue on GitHub

---

**Built with**: Docusaurus v3.6.3 | Node.js 20+ | TypeScript
**Deployed to**: GitHub Pages
**Maintained by**: [Your Name]
