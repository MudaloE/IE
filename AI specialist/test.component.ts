import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {
  currentPrompt: string = 'Describe a memorable holiday you’ve had.';
  timer: number = 0;

  constructor() {}

  ngOnInit(): void {}

  startTimer(): void {
    this.timer = 120; // 2 minutes
    const interval = setInterval(() => {
      if (this.timer > 0) {
        this.timer--;
      } else {
        clearInterval(interval);
        alert('Time is up!');
      }
    }, 1000);
  }
}
