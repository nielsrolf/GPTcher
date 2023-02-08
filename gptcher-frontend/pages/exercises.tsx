import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import Starfield from '../components/Starfield'

const Exercises = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  return (
    <div>
      <Starfield />
      <div id="content-wide">
        <Menu session={session} supabase={supabase} />
        <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '30vw'}} />
        <h1>Exercises</h1>
        <h2>coming soon</h2>
      </div>
    </div>
  )
}

export default Exercises
