import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Account from '../components/Account'
import Menu from '../components/Menu'

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  console.log({ session, supabase })

  return (
    <div className="container" style={{ padding: '50px 0 100px 0' }}>
      <Menu session={session} supabase={supabase} />
      {!session ? (
        <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} theme="dark" />
      ) : (
        <Account session={session} />
      )}
    </div>
  )
}

export default Home
