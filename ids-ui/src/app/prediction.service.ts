// prediction.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private baseUrl = 'http://127.0.0.1:5000'; // or your backend IP

  constructor(private http: HttpClient) {}

  // Function to call the /predict endpoint
  predict(features: number[]): Observable<any> {
    return this.http.post(`${this.baseUrl}/predict`, { features });
  }
}
