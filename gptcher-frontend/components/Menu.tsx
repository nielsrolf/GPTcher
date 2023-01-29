import Link from 'next/link'

import { useState } from 'react';

const Menu = ({ session, supabase }: any) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const handleSignOut = async () => {
    await supabase.auth.signOut()
  }

  return (
    <nav>
      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
        <img src="/GPTcher_Face_White.svg" alt="menu"  style={{height: '50px', width: '50px'}}/>
      </button>
      <Link href="/" className={menuOpen ? 'menu-open' : 'menu-closed'}>
        GPTcher
      </Link>
      {session ? (
        <>
          <Link href="/chat" className={menuOpen ? 'menu-open' : 'menu-closed'}>
            Chat
          </Link>
          <Link href="/training" className={menuOpen ? 'menu-open' : 'menu-closed'}>
            Training
          </Link>
          <Link href="/about" className={menuOpen ? 'menu-open' : 'menu-closed'}>
            About
          </Link>
          <a onClick={handleSignOut} className={menuOpen ? 'menu-open' : 'menu-closed'}>Sign out</a>
        </>
      ) : (
        <>
          <Link href="/about" className={menuOpen ? 'menu-open' : 'menu-closed'}>
            About
          </Link>
          <Link href="/chat" className={menuOpen ? 'menu-open' : 'menu-closed'}>
            Sign in / Sign up
          </Link>
        </>
      )}
    </nav>
  )
}

export default Menu