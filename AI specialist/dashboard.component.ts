import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  userData = {
    sessionsCompleted: 10,
    averageScore: 7.5,
  };

  constructor() {}

  ngOnInit(): void {}
}
