import React from 'react';
import parse from 'html-react-parser';


const TeacherMessage = React.forwardRef<HTMLDivElement, { message: { id: string, text: string, sender: string, text_en: string, text_translated: string, voice: string, created_at: string, session: string, evaluation: any, user_id: string } }>((props, ref) => {
    const { message } = props;
    const isUrl = message.text.startsWith("http") && message.text.endsWith(".mp3");
    return (
        <div key={message.id} className='teacher-msg-outer'>
            <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '50px', padding: '5px'}} />
            <div key={message.id} className='message-container teacher-message'  ref={ref}>
                {isUrl ? (
                    <audio controls>
                        <source src={message.text} type="audio/mpeg" />
                        Your browser does not support the audio element.
                    </audio>
                ) : (
                    <div>
                        {parse(message.text.replace('</b>', '</b><hr>'))}
                    </div>
                )}
                {message.text_en && (
                    <>
                        <hr />
                        <div>
                            {parse(message.text_en.replace('</b>', '</b><hr>'))}
                        </div>
                    </>
                )}
            </div>
        </div>
    )
});

export default TeacherMessage;
