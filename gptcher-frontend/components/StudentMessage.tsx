import React from 'react';
import parse from 'html-react-parser';


const StudentMessage = React.forwardRef<HTMLDivElement, { message: { id: string, text: string, sender: string, text_en: string, text_translated: string, voice: string, created_at: string, session: string, evaluation: any, user_id: string }, isExercise?: boolean }>((props, ref) => {
    const { message, isExercise } = props;
    return (
        <div key={message.id} className='teacher-msg-outer'>
            <img src="/Icon_YOU.svg" alt="GPTcher Logo" style={{float: 'right', width: '50px', padding: '5px'}} />
            <div key={message.id} className='message-container student-message' ref={ref}>
                <div>
                    {parse(message.text.replace('</b>', '</b><hr>'))}
                </div>
                {message.text_translated && isExercise !== true && (
                    <>
                        <hr />
                        <div>
                            {parse(message.text_translated.replace('</b>', '</b><hr>').replace('\n', '<br />'))}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
});

export default StudentMessage;
