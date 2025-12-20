/**
 * Custom Navbar Item Types
 * Extends Docusaurus default navbar items with custom types
 */
import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import UserNavbarItem from '@site/src/components/UserNavbarItem';
import { LanguageToggle } from '@site/src/components/LanguageToggle';

export default {
  ...ComponentTypes,
  'custom-user': UserNavbarItem,
  'custom-language': LanguageToggle,
};
