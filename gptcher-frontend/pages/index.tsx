import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import DemoCarousel from '@/components/DemoCarousel';

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  console.log({ session, supabase })

  return (
    <div id='content-wide'>
      <Menu session={session} supabase={supabase} />
      <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '30vw'}} />
      <h1>GPTcher</h1>
      <h2>Hola I'm a language tutor bot</h2>
      <DemoCarousel />
    </div>
  )
}

export default Home
