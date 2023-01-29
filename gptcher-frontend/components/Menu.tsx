import Link from 'next/link'

const Menu = ({ session, supabase }: any) => {
  const handleSignOut = async () => {
    await supabase.auth.signOut()
  }

  return (
    <nav>
      <Link href="/">
        GPTcher
      </Link>
      {session ? (
        <>
          <Link href="/chat">
            Chat
          </Link>
          <Link href="/training">
            Training
          </Link>
          <Link href="/about">
            About
          </Link>
          <a onClick={handleSignOut}>Sign out</a>
        </>
      ) : (
        <>
          <Link href="/about">
            About
          </Link>
          <Link href="/chat">
            Sign in / Sign up
          </Link>
        </>
      )}
    </nav>
  )
}

export default Menu
