import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import Starfield from '../components/Starfield'

const About = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  console.log({ session, supabase })

  return (
    <div>
      <Starfield />
      <div id="content">
        <Menu session={session} supabase={supabase} />
        <h1>About GPTcher</h1>
      </div>
    </div>
  )
}

export default About
