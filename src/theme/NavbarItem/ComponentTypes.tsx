/**
 * Custom Navbar Item Types
 * Extends Docusaurus default navbar items with custom 'user' type
 */
import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import UserNavbarItem from '@site/src/components/UserNavbarItem';

export default {
  ...ComponentTypes,
  'custom-user': UserNavbarItem,
};
