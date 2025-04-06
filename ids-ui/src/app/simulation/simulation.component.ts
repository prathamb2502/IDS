import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.css']
})
export class SimulationComponent {
  simulationOutput: string = '';

  constructor(private http: HttpClient) { }

  startSimulation() {
    this.http.post('http://localhost:5000/simulate', {})
      .subscribe((response: any) => {
        if (response.status === 'success') {
          this.simulationOutput = response.output;
        } else {
          this.simulationOutput = 'Error: ' + response.message;
        }
      });
  }
}
