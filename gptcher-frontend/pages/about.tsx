import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'

const About = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  console.log({ session, supabase })

  return (
    <div id="content">
      <Menu session={session} supabase={supabase} />
      <h1>About GPTcher</h1>
    </div>
  )
}

export default About
