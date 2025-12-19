/**
 * Custom Navbar Item - Shows Login button or User Avatar based on auth state
 */
import React, { useState, useEffect, useRef } from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

interface UserData {
  email: string;
  userId: string;
}

function getInitials(email: string): string {
  // Get initials from email (e.g., "asif@example.com" -> "AS")
  const name = email.split('@')[0];
  if (name.length >= 2) {
    return name.substring(0, 2).toUpperCase();
  }
  return name.toUpperCase();
}

export default function UserNavbarItem(): JSX.Element {
  const [user, setUser] = useState<UserData | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const loginUrl = useBaseUrl('/login');
  const docsUrl = useBaseUrl('/docs/intro');

  useEffect(() => {
    // Check if user is logged in
    const checkAuth = () => {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        const email = localStorage.getItem('user_email');
        const userId = localStorage.getItem('user_id');

        if (token && email && userId) {
          setUser({ email, userId });
        } else {
          setUser(null);
        }
      }
    };

    checkAuth();

    // Listen for storage changes (login/logout from other tabs)
    window.addEventListener('storage', checkAuth);

    // Custom event for same-tab login
    window.addEventListener('userLoggedIn', checkAuth);

    return () => {
      window.removeEventListener('storage', checkAuth);
      window.removeEventListener('userLoggedIn', checkAuth);
    };
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_id');
    setUser(null);
    setShowDropdown(false);
    window.location.href = docsUrl;
  };

  if (!user) {
    return (
      <Link to={loginUrl} className={styles.loginButton}>
        Login
      </Link>
    );
  }

  const initials = getInitials(user.email);

  return (
    <div className={styles.userContainer} ref={dropdownRef}>
      <button
        className={styles.avatarButton}
        onClick={() => setShowDropdown(!showDropdown)}
        title={user.email}
      >
        <span className={styles.avatar}>{initials}</span>
      </button>

      {showDropdown && (
        <div className={styles.dropdown}>
          <div className={styles.dropdownHeader}>
            <span className={styles.dropdownAvatar}>{initials}</span>
            <span className={styles.dropdownEmail}>{user.email}</span>
          </div>
          <div className={styles.dropdownDivider} />
          <button className={styles.logoutButton} onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
