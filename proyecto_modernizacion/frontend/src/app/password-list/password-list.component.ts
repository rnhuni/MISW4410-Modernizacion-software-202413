import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { IPassword } from '../models/password';
import { PasswordService } from './get.service';

@Component({
  selector: 'app-password-list',
  templateUrl: './password-list.component.html',
  styleUrls: ['./password-list.component.css']
})
export class PasswordListComponent {

  public passwords : Array<IPassword> = []

  constructor(private router: Router, private passwordService: PasswordService) { }

  ngOnInit() {
    this.getPasswords();
  }

  private getPasswords() : void {
    this.passwordService.getPasswords().subscribe(passwords => {
      passwords.forEach(element => {
        let password : IPassword = {
          name : element.nombre,
          password : element.clave,
          confirmPassword : element.clave,
          hint : element.pista
        }
        this.passwords.push(password)
      })
    })
  }

  goToCreatePassword() {
    this.router.navigate(['/create-password']);
  }
}
