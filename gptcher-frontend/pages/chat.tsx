import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Chat from '../components/Chat'
import Menu from '../components/Menu'
import { useEffect, useState } from 'react'

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()


  // if screen is > 500px, set width to 500px, else to 100%
  const [isMobile, setIsMobile] = useState(false);
    const checkMobile = () => {
        if (window.innerWidth < 600) {
            setIsMobile(true);
        } else {
            setIsMobile(false);
        }
    };

    useEffect(() => {
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    useEffect(() => {
      const starfield = document.getElementById("starfield");

      const generateStar = () => {
        const star = document.createElement("div");
        star.classList.add("star");
        star.style.top = Math.random() * 98 + "%";
        star.style.left = Math.random() * 98 + "%";
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
      <div id="content">
      <Menu session={session} supabase={supabase} />
      {!session ? (
        <div style={{width: isMobile ? '100%' : '500px', margin: '0 auto', minHeight: '60vh', marginTop: '20vh'}}>
          <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} theme="dark" />
        </div>
      ) : (
        <Chat session={session} />
      )}
    </div>
    </div>
    
  )
}

export default Home
