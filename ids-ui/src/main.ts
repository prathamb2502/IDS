import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { importProvidersFrom } from '@angular/core';
import { FormsModule } from '@angular/forms';

bootstrapApplication(AppComponent, {
  // Spread the existing appConfig properties and add additional providers
  ...appConfig,
  providers: [
    ...appConfig.providers,
    provideHttpClient(),
    importProvidersFrom(FormsModule)
  ]
}).catch((err) => console.error(err));
