import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SpeechService {
  startRecognition() {
    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = (event: any) => {
      console.log('Transcript:', event.results[0][0].transcript);
    };

    recognition.onerror = (error: any) => {
      console.error('Speech recognition error:', error);
    };
  }
}
