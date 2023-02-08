import React, { useState, useEffect } from 'react';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css";


const DemoCarousel = () => {
    const [isMobile, setIsMobile] = useState(false);
    const checkMobile = () => {
        if (window.innerWidth < 1000) {
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

    if(isMobile) {
        return (
            <Carousel
                showThumbs={false}
                showStatus={false}
                infiniteLoop={true}
                swipeable={isMobile}
                dynamicHeight={true}
                emulateTouch={isMobile}
                useKeyboardArrows={!isMobile}
            >
                <div>
                    <img src="screen1.png" className="image-rounded" alt="image1" />
                </div>
                <div>
                    <img src="intro_converse.png" className="image-rounded" alt="image2" />
                </div>
                <div>
                    <img src="exercises2.png" className="image-rounded" alt="image3" />
                </div>
            </Carousel>
        );
    } else {
        return (
            <div style={{display: 'flex', justifyContent: 'center', flexDirection: 'row', width: '95vw', alignContent: 'space-between'}}>
                <div>
                    <img src="screen1.png" className="image-rounded" alt="image1" />
                </div>
                <div>
                    <img src="intro_converse.png" className="image-rounded" alt="image2" />
                </div>
                <div>
                    <img src="exercises2.png" className="image-rounded" alt="image3" />
                </div>
            </div>
        );
    }
};

export default DemoCarousel;