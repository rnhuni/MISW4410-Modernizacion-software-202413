import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { IPassword, IPasswordRequest } from '../models/password';

@Injectable({
  providedIn: 'root'
})
export class PasswordService {

  private apiUrl : string = environment.apiUrl

  constructor(private http : HttpClient) { }

  public getPasswords() : Observable<IPasswordRequest[]> {
    return this.http.get<IPasswordRequest[]>(this.apiUrl);
  }
}
