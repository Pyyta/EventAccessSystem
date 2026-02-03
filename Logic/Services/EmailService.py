#EmailService: takes care of sending and creating emails 
from email.message import EmailMessage
import smtplib
import socket
from dotenv import load_dotenv
import os

class EmailService:
    def __init__(self):
        load_dotenv()
        self.email=EmailMessage()
        self.host_email= os.getenv("HOST_EMAIL")
        self.host_password= os.getenv("HOST_PASSWORD")
            
    def ticket_email_setter(self, user, ticket_buffer):
        first_name=user["name"].split()[0]
        self.email["From"]="noreply.nynya@gmail.com"
        self.email["To"] = user["email"]
        self.email["Subject"]="¡Bienvenido al clan, Nynya! Ya tienes tu lugar el 30 de agosto."
        message=f"""
                    Hola, {first_name},

                    Ya eres parte del movimiento. Tu registro para la próxima sesión de NYNYA COLLECTIVE ha sido procesado con éxito.

                    El 30 de agosto de 2026 bajamos la frecuencia para conectar con lo más crudo del House, UK Garage y Dubstep. La cabina está lista y tu lugar en la pista está asegurado.

                    --------------------------------------------------
                    📂 TU TICKET DE ACCESO:
                    Para ingresar al evento, es indispensable presentar tu entrada. La encontrarás adjunta en este correo en formato PDF.

                    > Recuerda: No es necesario imprimirlo; con que lo lleves descargado en tu celular para escanearlo en puerta es suficiente. Ahorremos papel, gastemos suelas.
                    --------------------------------------------------

                    Detalles del evento:
                    * Fecha: 30 de agosto, 2026.
                    * Apertura de puertas: 7:00
                    * Ubicación: ZONA 57 CLUB Cll 57 #42-11

                    Pronto recibirás más información sobre el line-up y los horarios de los sets. Mantente alerta.

                    See you in the dance.
                    — El equipo de NYNYA COLLECTIVE.
                    """
        self.email.set_content(message)
        html_content=f"""
                        <!DOCTYPE html>
                        <html lang="es">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>NYNYA Collective</title>
                        </head>
                        <body style="margin: 0; padding: 0; background-color: #0d1b1e; font-family: Arial, sans-serif; color: #ffffff;">

                            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; background-color: #0a1617; margin-top: 20px; border-top: 4px solid #3fd2a4;">
                                
                                <tr>
                                    <td align="center" style="padding: 40px 0 20px 0;">
                                        <h1 style="color: #3fd2a4; text-transform: uppercase; letter-spacing: 5px; margin: 0; font-size: 32px; border: 2px solid #3fd2a4; display: inline-block; padding: 10px 20px;">
                                            NYNYA<br>COLLECTIVE
                                        </h1>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 20px 40px; line-height: 1.6; color: #a5d1d1; font-size: 16px;">
                                        <p>Hola, <span style="color: #3fd2a4; font-weight: bold;">{first_name}</span>,</p>
                                        
                                        <p>Ya eres parte del movimiento. Tu registro para la próxima sesión de NYNYA ha sido procesado con éxito.</p>
                                        
                                        <p>El <strong>30 de agosto de 2026</strong>  bajamos la frecuencia para conectar con lo más crudo del House, UK Garage y Dubstep. La cabina está lista y tu lugar en la pista está asegurado.</p>

                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 0 40px 30px 40px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="border: 2px dashed #3fd2a4; border-radius: 10px; padding: 20px;">
                                            <tr>
                                                <td width="60" valign="top">
                                                    <img src="https://cdn-icons-png.flaticon.com/512/337/337946.png" alt="PDF" width="50" style="display: block; filter: invert(72%) sepia(54%) saturate(442%) hue-rotate(114deg) brightness(93%) contrast(89%);">
                                                </td>
                                                <td style="padding-left: 15px;">
                                                    <p style="font-size: 14px; color: #a5d1d1; margin: 5px 0; line-height: 1.4;">
                                                        Tu entrada digital ha sido generada y se encuentra adjunta a este correo. <br>
                                                        No olvides presentarla para ingresar al evento.
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 20px 40px; background-color: #081213; border-bottom: 4px solid #3fd2a4;">
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td align="left" style="font-size: 12px; color: #a5d1d1;">
                                                    <span style="color: #3fd2a4;">@</span> nynya.collective
                                                </td>
                                                <td align="center" style="font-size: 12px; color: #a5d1d1;">
                                                    <span style="color: #3fd2a4;">W:</span> 3222300951
                                                </td>
                                                <td align="right" style="font-size: 12px; color: #a5d1d1;">
                                                    <span style="color: #3fd2a4;">L:</span> Calle 56 #13-38
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>

                        </body>
                        </html>
                    """
        self.email.add_alternative(html_content, subtype="html")
        ticket_attached = self.add_ticket_to_email(ticket_buffer, user)
        if ticket_attached[0]: 
            email_state = self.email_connection_and_sending()
            return email_state
        else: return ticket_attached
        
    def admin_password_reset(self, admin_email, reset_pin):
        self.email["From"]="noreply.nynya@gmail.com"
        self.email["To"] = admin_email
        self.email["Subject"]="Pin de cinco digitos para la recuperación de contraseña"
        message=f"""Hola,

                    Se ha solicitado un cambio de contraseña para la cuenta de administrador,
                    debido a que la contraseña fue olvidada.

                    Para continuar con el proceso, utiliza el siguiente PIN de verificación:

                    PIN de administrador: {reset_pin}

                    Si no realizaste esta solicitud, ignora este correo o comunícate con el
                    soporte del sistema de inmediato.

                    Este es un mensaje automático, por favor no respondas a este correo."""
        self.email.set_content(message)
        if self.email_connection_and_sending()[0]:
            return (True, "Email sent")
    
    def add_ticket_to_email(self, ticket_buffer, user):
        try:
            ticket_buffer.seek(0)
            ticket_data = ticket_buffer.read() 
            self.email.add_attachment(
                ticket_data,
                maintype="application",
                subtype="pdf",
                filename=f"{user['document']} Ticket.pdf" 
            )
            return (True, "Ticket added successfully")     
        except Exception as e:
            return (False, f"Error processing buffer: {str(e)}")

    
    def email_connection_and_sending(self):
        try:
            with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as server:
                server.login(user=self.host_email, password=self.host_password)
                server.send_message(self.email)
            return (True, "Success")
        except smtplib.SMTPRecipientsRefused:
            return (False, "Email Not Found")
        except socket.gaierror:
            return (False, "Connection Failed")
        except socket.timeout:
            return (False, "Timeout error")
        except smtplib.SMTPAuthenticationError:
            return (False, "Host authentication error")



