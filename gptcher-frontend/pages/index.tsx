import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import DemoCarousel from '@/components/DemoCarousel';
import { useEffect } from 'react'
import Starfield from '../components/Starfield';

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  return (
    <div>
      <Starfield />
      <div id='content-wide'>
        <Menu session={session} supabase={supabase} />
        <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '30vw'}} />
        <h1>GPTcher</h1>
        <h2>Hola I'm a language tutor bot</h2>
        <p>
          Learn by conversing with an AI teacher, do exercises, train your vocabulary and give us feedback! This project is in beta, so please be patient with us.
        </p>
        <DemoCarousel />
      </div>
    </div>
  )
}

export default Home
