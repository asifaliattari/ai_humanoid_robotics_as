import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Feature cards with images
const features = [
  {
    title: 'ROS 2 & Navigation',
    description: 'Master the Robot Operating System 2 for building robust, real-time robotic applications.',
    image: 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=300&fit=crop',
    link: 'docs/modules/ros2/',
  },
  {
    title: 'Digital Twin Simulation',
    description: 'Create virtual replicas of robots for testing, training, and optimization.',
    image: 'https://images.unsplash.com/photo-1558346490-a72e53ae2d4f?w=400&h=300&fit=crop',
    link: 'docs/modules/digital-twin/',
  },
  {
    title: 'NVIDIA Isaac',
    description: 'Leverage GPU-accelerated simulation and AI for next-gen robotics.',
    image: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=300&fit=crop',
    link: 'docs/modules/isaac/',
  },
  {
    title: 'Vision-Language-Action',
    description: 'Train robots with multimodal AI that understands vision, language, and actions.',
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=300&fit=crop',
    link: 'docs/modules/vla/',
  },
  {
    title: 'Hardware Integration',
    description: 'Connect simulation to real hardware with Jetson, sensors, and actuators.',
    image: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=300&fit=crop',
    link: 'docs/hardware/',
  },
  {
    title: 'AI-Powered Chatbot',
    description: 'Ask questions and get instant answers from the textbook with our RAG chatbot.',
    image: 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=400&h=300&fit=crop',
    link: 'docs/ai-features/',
  },
];

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className={styles.heroBackground}>
        <img
          src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&h=800&fit=crop"
          alt="Humanoid Robot"
          className={styles.heroImage}
        />
        <div className={styles.heroOverlay} />
      </div>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          {siteConfig.title}
        </Heading>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="docs/intro">
            Start Learning
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="docs/foundations/">
            View Foundations
          </Link>
        </div>
        <div className={styles.stats}>
          <div className={styles.stat}>
            <span className={styles.statNumber}>6</span>
            <span className={styles.statLabel}>Core Modules</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statNumber}>145+</span>
            <span className={styles.statLabel}>Searchable Topics</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statNumber}>AI</span>
            <span className={styles.statLabel}>Powered Chatbot</span>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({title, description, image, link}) {
  return (
    <div className={clsx('col col--4', styles.featureCard)}>
      <Link to={link} className={styles.featureLink}>
        <div className={styles.featureImageWrapper}>
          <img src={image} alt={title} className={styles.featureImage} />
          <div className={styles.featureImageOverlay} />
        </div>
        <div className={styles.featureContent}>
          <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
          <p className={styles.featureDescription}>{description}</p>
          <span className={styles.featureArrow}>Explore &rarr;</span>
        </div>
      </Link>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2" className={styles.sectionTitle}>
            What You'll Learn
          </Heading>
          <p className={styles.sectionSubtitle}>
            A comprehensive curriculum covering everything from ROS 2 fundamentals to advanced AI-powered humanoid robotics
          </p>
        </div>
        <div className="row">
          {features.map((props, idx) => (
            <FeatureCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function HomepageCTA() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <div className={styles.ctaContent}>
          <Heading as="h2" className={styles.ctaTitle}>
            Ready to Build the Future?
          </Heading>
          <p className={styles.ctaDescription}>
            Start your journey into humanoid robotics today. Our AI-powered textbook adapts to your learning style.
          </p>
          <div className={styles.ctaButtons}>
            <Link
              className="button button--primary button--lg"
              to="docs/intro">
              Get Started Free
            </Link>
            <Link
              className="button button--outline button--lg"
              to="docs/ai-features/">
              Try AI Chatbot
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function AuthorSection() {
  return (
    <section className={styles.authorSection}>
      <div className="container">
        <div className={styles.authorContent}>
          <div className={styles.authorInfo}>
            <Heading as="h2" className={styles.authorTitle}>
              About the Author
            </Heading>
            <h3 className={styles.authorName}>Asif Ali</h3>
            <p className={styles.authorBio}>
              Passionate about AI, Robotics, and building the future of autonomous systems.
            </p>
          </div>
          <div className={styles.socialLinks}>
            <a href="mailto:asif.alimusharaf@gmail.com" className={styles.socialLink} title="Email">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
              </svg>
              <span>Email</span>
            </a>
            <a href="https://linkedin.com/in/asif-ali-a1879a2ba" target="_blank" rel="noopener noreferrer" className={styles.socialLink} title="LinkedIn">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
              <span>LinkedIn</span>
            </a>
            <a href="https://github.com/asifaliattari" target="_blank" rel="noopener noreferrer" className={styles.socialLink} title="GitHub">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
              </svg>
              <span>GitHub</span>
            </a>
            <a href="https://youtube.com/@AstolixGen" target="_blank" rel="noopener noreferrer" className={styles.socialLink} title="YouTube">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                <path d="M10 15l5.19-3L10 9v6m11.56-7.83c.13.47.22 1.1.28 1.9.07.8.1 1.49.1 2.09L22 12c0 2.19-.16 3.8-.44 4.83-.25.9-.83 1.48-1.73 1.73-.47.13-1.33.22-2.65.28-1.3.07-2.49.1-3.59.1L12 19c-4.19 0-6.8-.16-7.83-.44-.9-.25-1.48-.83-1.73-1.73-.13-.47-.22-1.1-.28-1.9-.07-.8-.1-1.49-.1-2.09L2 12c0-2.19.16-3.8.44-4.83.25-.9.83-1.48 1.73-1.73.47-.13 1.33-.22 2.65-.28 1.3-.07 2.49-.1 3.59-.1L12 5c4.19 0 6.8.16 7.83.44.9.25 1.48.83 1.73 1.73z"/>
              </svg>
              <span>YouTube</span>
            </a>
            <a href="tel:+923302541908" className={styles.socialLink} title="Phone">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
              </svg>
              <span>+92 330 2541908</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="AI-native textbook for building autonomous humanoid robots with ROS 2, Isaac, and VLA systems">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <HomepageCTA />
        <AuthorSection />
      </main>
    </Layout>
  );
}
