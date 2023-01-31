import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import DemoCarousel from '@/components/DemoCarousel';
import { useEffect } from 'react'

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()


  useEffect(() => {
    const starfield = document.getElementById("starfield");

    const generateStar = () => {
      const star = document.createElement("div");
      star.classList.add("star");
      star.style.top = Math.random() * 100 + "%";
      star.style.left = Math.random() * 100 + "%";
      star.style.width = Math.random() * 2 + 1 + "px";
      star.style.height = star.style.width;
      star.style.opacity = Math.random();
      starfield.appendChild(star);
      
      setTimeout(() => {
        star.style.opacity = 0;
        setTimeout(() => {
          star.remove();
          generateStar();
        }, 500);
      }, Math.random() * 10000);
    }

    for (let i = 0; i < 100; i++) {
      generateStar();
    }
  }, []);

  return (
    <div>
      <div id="starfield"></div>
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
