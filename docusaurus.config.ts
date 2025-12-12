import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// GitHub configuration
const githubUsername = 'asifaliattari';
const repoName = 'ai_humanoid_robotics_as';

// Detect deployment environment
const isVercel = process.env.VERCEL === '1';
const siteUrl = isVercel
  ? (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'https://ai-humanoid-robotics-as.vercel.app')
  : `https://${githubUsername}.github.io`;
const baseUrl = isVercel ? '/' : `/${repoName}/`;

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-native textbook for building autonomous humanoid robots with ROS 2, Isaac, and Vision-Language-Action systems',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: siteUrl,
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel: '/', For GitHub Pages: '/<projectName>/'
  baseUrl: baseUrl,

  // GitHub pages deployment config.
  organizationName: githubUsername,
  projectName: repoName,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: `https://github.com/${githubUsername}/${repoName}/tree/main/`,
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl: `https://github.com/${githubUsername}/${repoName}/tree/main/`,
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Robot Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'bookSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          type: 'doc',
          docId: 'foundations/index',
          position: 'left',
          label: 'Foundations',
        },
        {
          type: 'dropdown',
          label: 'Modules',
          position: 'left',
          items: [
            {
              type: 'doc',
              docId: 'modules/ros2/index',
              label: 'Module 1: ROS 2',
            },
            {
              type: 'doc',
              docId: 'modules/digital-twin/index',
              label: 'Module 2: Digital Twin',
            },
            {
              type: 'doc',
              docId: 'modules/isaac/index',
              label: 'Module 3: Isaac',
            },
            {
              type: 'doc',
              docId: 'modules/vla/index',
              label: 'Module 4: VLA',
            },
          ],
        },
        {
          type: 'doc',
          docId: 'hardware/index',
          position: 'left',
          label: 'Hardware',
        },
        {
          type: 'doc',
          docId: 'capstone/index',
          position: 'left',
          label: 'Capstone',
        },
        {
          type: 'doc',
          docId: 'ai-features/index',
          position: 'left',
          label: 'AI Features',
        },
        {to: '/blog', label: 'Blog', position: 'right'},
        {
          href: `https://github.com/${githubUsername}/${repoName}`,
          label: 'GitHub',
          position: 'right',
        },
        {
          to: 'login',
          label: 'Login',
          position: 'right',
          className: 'login-button',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: `https://github.com/${githubUsername}/${repoName}`,
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus and Claude Code.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
