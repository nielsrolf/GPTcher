import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Chat from '../components/Chat'
import Menu from '../components/Menu'

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  console.log({ session, supabase })

  return (
    <div id="content-wide">
      <Menu session={session} supabase={supabase} />
      {!session ? (
        <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} theme="dark" />
      ) : (
        <Chat session={session} />
      )}
    </div>
  )
}

export default Home
