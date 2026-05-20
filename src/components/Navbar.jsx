import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container container">
        <NavLink to="/" className="navbar-logo" onClick={() => setIsOpen(false)}>
          <img src="/logo.png" alt="Parafarmacia Viale Umberto 1°" className="logo-img" />
          <div className="logo-text">
            <span>Parafarmacia</span>
            <span>Viale Umberto 1°</span>
          </div>
        </NavLink>

        <div className="menu-icon" onClick={toggleMenu}>
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </div>

        <ul className={isOpen ? 'nav-menu active' : 'nav-menu'}>
          <li className="nav-item">
            <NavLink to="/" className="nav-links" onClick={() => setIsOpen(false)}>
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/servizi" className="nav-links" onClick={() => setIsOpen(false)}>
              Servizi
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/tisane" className="nav-links" onClick={() => setIsOpen(false)}>
              Le Nostre Tisane
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/contatti" className="nav-links" onClick={() => setIsOpen(false)}>
              Contatti
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
