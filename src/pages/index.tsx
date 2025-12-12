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
      </main>
    </Layout>
  );
}
