// prediction.component.ts
import { Component } from '@angular/core';
import { PredictionService } from '../prediction.service';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent {
  // This variable will store the user-input features.
  // For this example, we'll assume a single numeric feature.
  featureInput: number = 0;
  predictionResult: any = null;
  errorMessage: string = '';

  constructor(private predictionService: PredictionService) {}

  // Function to call the predict endpoint
  makePrediction() {
    this.predictionService.predict([this.featureInput]).subscribe(
      (response: any) => {
        this.predictionResult = response.prediction;
        this.errorMessage = '';
      },
      (error) => {
        console.error('Prediction error:', error);
        this.errorMessage = 'Error making prediction. Please try again.';
        this.predictionResult = null;
      }
    );
  }
}
